from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from Courses.models import Course
from Exams.models import Exam
from Exams.forms import ExamForm
from Enrollments.models import Enrollment
from Students.models import Student
from Users.models import User
from Teachers.models import Teacher
from main.views import get_user
import json
from main.views import timer, get_time_now
import datetime

def order(exam, status):
    status_order = {
        'inprogress': 1,
        'waiting': 2,
        'ended': 3
    }.get(status, 4)
    if (status_order == 1):
        return (status_order, exam.EndTime)
    return (status_order, exam.StartTime)

@timer
def course_page(request, course_id):
    user_pk = request.session.get('user_id')
    if (not user_pk):
        return redirect("Users:login")
    user = get_user(request)

    cache_key = f'course_{course_id}'
    course = cache.get(cache_key)
    if not course:
        course = get_object_or_404(Course, pk=course_id)
        cache.set(cache_key, course, 3600)

    if (user.Role == "student"):
        try:
            if not(Enrollment.objects.filter(StudentKey=user.pk, CourseKey=course.pk).exists()):
                return render(request, 'Courses/not_allowed.html')
        except Exception:
            raise Http404("خطای نامشخص - لطفا دوباره امتحان کنید")
    elif (user.Role == "teacher"):
        if (course.TeacherKey_id != user.teacher.pk):
            return render(request, 'Courses/not_allowed.html')
    
    exams = Exam.objects.filter(CourseKey=course_id)
    now = get_time_now()

    statuses = [
        'waiting' if now < exam.StartTime else
        'ended'  if now > exam.EndTime else
        'inprogress'
        for exam in exams
    ]
    ids = list(range(len(exams)))
    exams_with_status = list(zip(exams, statuses, ids))
    exams_with_status.sort(key=lambda data: order(data[0], data[1]))

    exams_data = []
    for exam, status, id in exams_with_status:
        exams_data.append({
            'id': exam.pk,
            'title': exam.Title,
            'start_time': exam.StartTime.isoformat() if exam.StartTime else None,
            'end_time': exam.EndTime.isoformat() if exam.EndTime else None,
            'status': status,
            # 'index': exam.pk,
        })

    context = {
        'course': course,
        'exams_with_status': exams_with_status,
        'for_js': json.dumps(exams_data),
        'role': user.Role,
        'form': ExamForm,
    }

    return render(request, 'Courses/page.html', context)