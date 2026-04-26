from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import datetime, timedelta
from django.utils import timezone
from main.views import get_user
from Exams.models import Exam
from Enrollments.models import Enrollment
from Courses.models import Course
from Users.models import User
from Students.models import Student
from Teachers.models import Teacher
from Questions.models import Question
from LoginSessions.models import LoginSession
from main.constant import Colors
from main.views import to_miladi, timer, get_time_now
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from .forms import ExamForm
import json, time, jdatetime, datetime

def exam_status(request, course_id, exam_id, user):
    cache_key = f'course_{course_id}'
    course = cache.get(cache_key)
    if not course:
        course = get_object_or_404(Course, pk=course_id)
        cache.set(cache_key, course, 10800)

    if (course.TeacherKey_id != user.teacher.pk):
            return render(request, 'Courses/not_allowed.html')
    
    students = LoginSession.objects.filter(ExamKey=exam_id).values('StudentKey__StudentNumber').annotate(count=Count('pk'))

    context = {
        'students': students
    }
    return context

def validate_teacher(request, course):
    role = request.session.get('role')
    user_id = request.session.get('user_id')
    if (role != 'teacher'):
        return False
    
    if (course.TeacherKey.UserKey_id != user_id):
        return False
    return True

@timer
def create_exam(request, course_id):
    if request.method == 'POST':
        cache_key = f'course_{course_id}'
        course = cache.get(cache_key)
        if not course:
            try:
                course = Course.objects.get(pk=course_id)
                cache.set(cache_key, course, 10800)
            except Exception:
                return JsonResponse({
                    'success': False,
                    'message': 'خطای نامشخص'
                })
        if not(validate_teacher(request, course)):
            return JsonResponse({
                'success': False,
                'message': 'دسترسی غیرمجاز'
            })
        form = ExamForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']
            start_datetime = to_miladi(start_date, start_time)
            end_datetime = (to_miladi(end_date, end_time))
            duration = int((end_datetime - start_datetime).total_seconds() / 60)
            new_exam = Exam.objects.create(
                CourseKey=course,
                TeacherKey=course.TeacherKey,
                Title=title,
                StartTime=start_datetime,
                EndTime=end_datetime,
                Duration = duration,
                Description=description,
            )
            now = get_time_now()
            data = {
                'id': new_exam.pk,
                'title': new_exam.Title,
                'start_time': new_exam.StartTime.isoformat() if new_exam.StartTime else None,
                'end_time': new_exam.EndTime.isoformat() if new_exam.EndTime else None,
                'status': 'waiting' if now < new_exam.StartTime else 'ended'  if now > new_exam.EndTime else 'inprogress',
                # 'index': 'new',
            }
            # j_date = jdatetime.datetime.fromgregorian(date=start_datetime)

            # print(f'{Colors.INFO}{start_datetime}{Colors.RESET}')
            # print(f'{Colors.INFO}{get_time_now()}{Colors.RESET}')
            # print(f'{Colors.INFO}{datetime.datetime.now()}{Colors.RESET}')
            # print(j_date)

            return JsonResponse({
                'success': True,
                'message': 'آزمون با موفقیت ایجاد شد.',
                'new_exam': data,
            })

        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list

        return JsonResponse({
            'success': False,
            'errors': errors,
        }, status=400)
    
    return JsonResponse({
        'success': False,
    })

def edit_exam(request, course_id, exam_id):
    return render(request, 'Exams/EditExam.html')

def delete_exam(request, course_id):
    cache_key = f'course_{course_id}'
    course = cache.get(cache_key)
    if not course:
        try:
            course = Course.objects.get(pk=course_id)
            cache.set(cache_key, course, 10800)
        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'خطای نامشخص'
            })
    if not(validate_teacher(request, course)):
        return JsonResponse({
            'success': False,
            'message': 'دسترسی غیرمجاز'
        })
    data = json.loads(request.body)
    exam_id = data.get('exam_id')
    Exam.objects.filter(pk=exam_id).delete()

    return JsonResponse({
        'status': 'success',
        'message': 'آزمون با موفقیت حذف شد.'
    })



@timer
def exam_page(request, course_id, exam_id):
    user = get_user(request)
    full_name = str(user.FirstName) + " " + str(user.LastName)
    full_name = full_name[::-1]

    cache_key = f'course_{course_id}'
    course = cache.get(cache_key)
    if not course:
        course = get_object_or_404(Course, pk=course_id)
        cache.set(cache_key, course, 10800)

    if not(Exam.objects.filter(pk=exam_id, CourseKey=course_id).exists()):
        return render(request, 'Exams/not_allowed.html')

    if (user.Role == 'student'):
        try:
            if not(Enrollment.objects.filter(StudentKey=user.pk, CourseKey=course.pk).exists()):
                return render(request, 'Courses/not_allowed.html')
        except Exception:
            raise Http404('خطای نامشخص - لطفا دوباره امتحان کنید')
        
        
        for i in range(2):
            try:
                login_session, created = LoginSession.objects.get_or_create(
                    StudentKey_id=user.pk,
                    ExamKey_id=exam_id,
                    IsActive=True,
                )
                break
            except MultipleObjectsReturned:
                LoginSession.objects.filter(
                    StudentKey_id=user.pk,
                    ExamKey_id=exam_id,
                    IsActive=True,
                ).update(IsActive=False)


        # if 'exam_session_id' in request.session:
        #     if not(created):
        #         login_session.IsActive = False
        #     return redirect('Courses:course_page', course_id)
        if (created):
            login_session.LoginTime = get_time_now()
            login_session.save(update_fields=['LoginTime'])
            request.session['exam_session_id'] = login_session.pk
            request.session['exam_id'] = exam_id
            request.session['last_time'] = time.time()
            print(f'{Colors.SUCCESS}[SUCCESS]: User {full_name} entered exam {exam_id} successfully{Colors.RESET}')
            
            
        else:
            login_session.IsActive = False
            login_session.LogoutTime = get_time_now()
            login_session.save(update_fields=['IsActive', 'LogoutTime'])
            request.session.pop('exam_session_id', None)
            request.session.pop('last_time', None)
            request.session.pop('started_exam', None)
            return redirect('Courses:course_page', course_id)
            new = LoginSession.objects.create(
                StudentKey=user.student,
                ExamKey_id=exam_id,
                IsActive=True,
            )
            login_session.LoginTime = get_time_now()
            login_session.save(update_fields=['LoginTime'])
            request.session['exam_session_id'] = login_session.pk
            request.session['last_time'] = time.time()
            print(f'{Colors.SUCCESS}[SUCCESS]: User {full_name} entered exam {exam_id} successfully{Colors.RESET}')
            print(f'{Colors.WARNING}[WARNING]: User {full_name} returned to exam {exam_id}{Colors.RESET}')
            # login_session.IsActive = False
            # login_session.save(update_fields=['IsActive'])

            pass

        context = {
            'exam_id': exam_id,
            'course_id': course_id,
            'last_page': True,
        }
        response = render(request, 'Exams/ExamPage.html', context)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        return render(request, 'Exams/ExamPage.html', context)

    elif (user.Role == 'teacher'):
        context = exam_status(request, course_id, exam_id, user)
        return render(request, 'Exams/ExamStatus.html', context)
    
        
def question_page(request, exam_id, course_id):
    if 'started_exam' not in request.session:
        request.session['started_exam'] = True
    else:
        return redirect('Courses:course_page', course_id)
    question = Question.objects.filter(ExamKey_id=exam_id)
    request.session['question_order'] = 1
    context = {
        'last_page': True,
        'question': question,
    }
    response = render(request, 'Exams/QuestionView.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
    return render(request, 'Exams/QuestionView.html', context)

    

@timer
@require_POST
def exit_exam(request):
    # start = time.perf_counter_ns()
    time.sleep(0.2)
    user = get_user(request)
    full_name = str(user.FirstName) + " " + str(user.LastName)
    full_name = full_name[::-1]
    
    if (user.Role == 'student'):

        try:
            login_session = LoginSession.objects.get(StudentKey=user.pk, ExamKey=request.session.get('exam_id'), IsActive=True)

        except ObjectDoesNotExist:
            print(f'{Colors.WARNING}[WARNING]: User {full_name} reloaded exam page{Colors.RESET}')
        
        try:
            if (login_session.IsActive == True):
                try:
                    data_received = json.loads(request.body)
                    data = {
                        'status': 'ok',
                        'message': 'successfully exited',
                        'course_id': login_session.ExamKey.CourseKey.pk
                    }

                    event = data_received.get('event')
                    login_session.IsActive = False
                    login_session.LogoutTime = get_time_now()
                    login_session.save(update_fields=['IsActive', 'LogoutTime'])
                    request.session.pop('exam_session_id', None)
                    request.session.pop('exam_id', None)
                    request.session.pop('last_time', None)
                    request.session.pop('started_exam', None)
                    if (event == 'exit_exam_without_click'):
                        print(f'{Colors.WARNING}[WARNING]: User {full_name} exited from exam {login_session.ExamKey.pk} without clicling exit exam button! perhaps closed browser window{Colors.RESET}')
                    else:
                        
                        print(f'{Colors.SUCCESS}[SUCCESS]: User {full_name} exited from exam {login_session.ExamKey.pk} succesfully{Colors.RESET}')
                    # additional = '(without clicling exit exam button! perhaps closed browser window)' if (event == 'exit_exam_without_click') else ''
                    # print(f'[LOG]: User {user} exited from exam {login_session.ExamKey.pk}', additional)
                    # end = time.perf_counter_ns()
                    # print(f'{Colors.INFO}[INFO]: executing time: {(end - start)} nanosecond{Colors.RESET}')
                    # print(f'{Colors.INFO}[INFO]: executing time: {(end - start) / 1000} microsecond{Colors.RESET}')
                    # print(f'{Colors.INFO}[INFO]: executing time: {(end - start) / 1_000_000} milisecond{Colors.RESET}')

                    return JsonResponse(data)    
                except json.JSONDecodeError:
                    data = {
                        'status': 'error',
                        'message': 'Invalid JSON'
                    }
                    return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
                
            else:
                data = {
                    'status': 'error',
                    'message': 'شما قبلا وارد این آزمون نشده‌اید'
                }
                return JsonResponse(data)

        except Exception:
            return JsonResponse({
                'status': 'unknown',
                'message': 'این آزمون برای شما تعریف نشده است'
            })
    else:
        return JsonResponse({
            'status': 'not student',
            'message': 'شما دانش آموز نیستید'
        })
