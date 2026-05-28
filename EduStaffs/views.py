from Users.decorators import session_login_required
from django.shortcuts import render, redirect, get_object_or_404 , redirect
from .models import EduStaff
from django.contrib import messages
from .forms import CourseCreateForm, EnrollStudentForm
from Courses.models import Course
from Enrollments.models import Enrollment
from Students.models import Student
from Teachers.models import Teacher
from django.db import connection
from django.utils import timezone

@session_login_required
def dashboard(request):
    user_id = request.session.get('user_id')

    try:
        edustaff = EduStaff.objects.select_related('DepartmentKey').get(UserKey_id=user_id)
    except EduStaff.DoesNotExist:
        return redirect('main:mainpage')

    return render(request, 'EduStaffs/dashboard.html', {
        'edustaff': edustaff,
        'department': edustaff.DepartmentKey
    })


def course_create(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("Users:login")

    try:
        staff = EduStaff.objects.select_related("DepartmentKey").get(UserKey_id=user_id)
    except EduStaff.DoesNotExist:
        return render(request, "Courses/not_allowed.html")
    
    if request.method == "POST":
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
     
            course.DepartmentKey = staff.DepartmentKey
            course.save()
            messages.success(request, "کلاس با موفقیت ایجاد شد.")
            return redirect("EduStaffs:dashboard")
    else:
        form = CourseCreateForm()

    return render(request, "EduStaffs/course_create.html", {
        "form": form, 
        "department": staff.DepartmentKey
    })

@session_login_required
def manage_courses(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("Users:login")

    try:
        staff = EduStaff.objects.select_related("DepartmentKey").get(UserKey_id=user_id)
    except EduStaff.DoesNotExist:
        return render(request, "Courses/not_allowed.html")

    courses = Course.objects.filter(DepartmentKey=staff.DepartmentKey).order_by("CourseName")

    return render(request, "EduStaffs/manage_courses.html", {
        "courses": courses,
        "department": staff.DepartmentKey,
        "staff": staff,
    })


def manage_enrollments(request, course_id):
    
    # # if not request.user.is_authenticated or request.user.Role != 'EduStaff':
    # # if not request.user.is_authenticated :
    # #     return redirect('Users:login')
    
    # course = get_object_or_404(Course, CourseID=course_id)
    
    # enrolled_students = Enrollment.objects.filter(CourseKey=course).select_related('StudentKey__UserKey')

    # if request.method == 'POST':
    #     form = EnrollStudentForm(request.POST)
    #     if form.is_valid():
    #         student = form.cleaned_data['student']
           
    #         if not Enrollment.objects.filter(CourseKey=course, StudentKey=student).exists():
    #             Enrollment.objects.create(CourseKey=course, StudentKey=student)
    #         return redirect('EduStaffs:manage_enrollments', course_id=course.CourseID)
    # else:
    #     form = EnrollStudentForm()

    # context = {
    #     'course': course,
    #     'enrolled_students': enrolled_students,
    #     'form': form
    # }
    # return render(request, 'EduStaffs/manage_enrollments.html', context)

    course = get_object_or_404(Course, CourseID=course_id)
    
    # --- نمایش دانشجویان ثبت نام شده ---
    # برای جلوگیری از خطای 'Unknown column 'Enrollments.id'', اینجا از raw query استفاده می کنیم
    enrolled_students_data = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.UserKey, 
                    u.Username,
                    u.FirstName, 
                    u.LastName, 
                    e.EnrolledAt, 
                    e.Grade, 
                    e.Status,
                    e.StudentKey, 
                    e.CourseKey,
                    s.StudentNumber
                FROM Enrollments e
                JOIN Students s ON e.StudentKey = s.UserKey  
                JOIN Users u ON s.UserKey = u.UserID 
                WHERE e.CourseKey = %s
                ORDER BY e.EnrolledAt DESC
            """, [course_id])
            rows = cursor.fetchall()
            
            columns = [desc[0] for desc in cursor.description]
            for row in rows:
                student_data = dict(zip(columns, row))
                enrolled_students_data.append(student_data)

    except Exception as e:
        messages.error(request, f"خطا در بارگیری لیست دانشجویان: {e}")
      
    if request.method == 'POST':
        form = EnrollStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('student') # استفاده از .get برای امنیت بیشتر
            
            if student:
                # print(f"DEBUG: Selected student object: {student}")
                # print(f"DEBUG: Student PK: {student.pk if student else 'None'}")
                # if hasattr(student, 'UserKey'):
                #     print(f"DEBUG: Student UserKey object: {student.UserKey}")
                #     print(f"DEBUG: Student UserKey ID: {student.UserKey.UserID}")
                
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO Enrollments (StudentKey, CourseKey, EnrolledAt, Status)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE Status='active' -- اگر دانشجو قبلا ثبت نام شده، وضعیت را فعال کن
                        """, [student.pk, course.CourseID, timezone.now(), "active"]) 
                    messages.success(request, f"دانشجو {student.UserKey.FirstName} با موفقیت به درس اضافه شد.")
                    return redirect('EduStaffs:manage_enrollments', course_id=course.CourseID)
                except Exception as e:
                    messages.error(request, f"خطا در ثبت نام دانشجو: {e}")
            else:
                 messages.error(request, "دانشجوی معتبر انتخاب نشده است.")
        else:
            messages.error(request, "اطلاعات فرم معتبر نیست.")
            
    else:
        form = EnrollStudentForm()

    context = {
        'course': course,
        'enrolled_students': enrolled_students_data, 
        'form': form
    }
    
    return render(request, 'EduStaffs/manage_enrollments.html', context)


def remove_student_from_course(request, course_id, student_id):
    # # enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    # # course_id = enrollment.CourseKey.CourseID
    # # enrollment.delete()
    # # return redirect('EduStaffs:manage_enrollments', course_id=course_id)

    # course = get_object_or_404(Course, CourseID=course_id)
    # student = get_object_or_404(Student, StudentID=student_id)

    # Enrollment.objects.filter(
    #     CourseKey=course,
    #     StudentKey=student
    # ).delete()

    # return redirect('EduStaffs:manage_enrollments', course_id=course.CourseID)

    course = get_object_or_404(Course, CourseID=course_id)
    
    # --- رفع مشکل StudentID ---
    # student_id که از URL می آید، باید همان UserKey باشد چون PK جدول Student است.
    try:
        student = Student.objects.get(pk= student_id) 
    except Student.DoesNotExist:
        messages.error(request, "دانشجوی مورد نظر یافت نشد.")
        return redirect('EduStaffs:manage_enrollments', course_id=course_id)
    except Exception as e:
        messages.error(request, f"خطا در یافتن دانشجو: {e}")
        return redirect('EduStaffs:manage_enrollments', course_id=course_id)
    # --- ---

    # --- استفاده از raw SQL برای DELETE ---
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Enrollments
                WHERE StudentKey = %s AND CourseKey = %s
            """, [student.pk, course.CourseID]) # student.pk باید همان UserKey باشد
        
        # --- نمایش پیام موفقیت ---
        try:
            student_name = f"{student.UserKey.FirstName} {student.UserKey.LastName}"
        except AttributeError:
            student_name = "دانشجو" # Fallback اگر نام قابل دسترسی نبود
        messages.success(request, f"دانشجو {student_name} با موفقیت از درس حذف شد.")
        # --- ---
        
    except Exception as e:
        messages.error(request, f"خطا در حذف دانشجو از درس: {e}")

    return redirect('EduStaffs:manage_enrollments', course_id=course.CourseID)

def assign_teacher_to_course(request, course_id):
    course = get_object_or_404(Course, CourseID=course_id)
    teachers = Teacher.objects.select_related('UserKey').all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(Teacher, pk=teacher_id)

        course.TeacherKey = teacher
        course.save()

        return redirect('EduStaffs:manage_courses')

    return render(request, 'EduStaffs/assign_teacher.html', {
        'course': course,
        'teachers': teachers,
    })