from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from Users.models import User
from Students.models import Student
from Enrollments.models import Enrollment
from Courses.models import Course
from Teachers.models import Teacher
import datetime, jdatetime
from main.constant import Colors
import time

def mainpage(request):
    user_pk = request.session.get('user_id')
    user = None
    fk = None
    courses = None
    if (user_pk):
        try :
            user = User.objects.select_related('student').get(pk=user_pk)
        except:
            return redirect("Users:login")    
        if (user.Role == "Student" or user.Role == "student"):
            # fk = Student.objects.get(UserKey=user_pk)
            fk = user.student
            courses = Course.objects.filter(enrollment__StudentKey=user_pk).distinct()
            # SELECT DISTINCT c.* FROM Course AS c JOIN Enrollment AS e ON e.CourseKey = c.CourseID WHERE e.StudentKey = <StudentID>;
        elif (user.Role == "teacher" or user.Role == "Teacher"):
            courses = Course.objects.filter(TeacherKey_id=user_pk)

    context = {
        'user': user,
        'fk': fk,
        'courses': courses, 
    }
    return render(request, 'main/index.html', context)

def get_user(request):
    user_pk = request.session.get('user_id')
    if (not user_pk):
        return redirect("Users:login")
    
    try:
        # user = User.objects.select_related("teacher", "student").get(pk=user_pk)
        user = User.objects.get(pk=user_pk)
    except ObjectDoesNotExist:
        return redirect("Users:login")
    except Exception:
        raise Http404("خطای نامشخص - لطفا دوباره امتحان کنید")
    
    return user

def to_miladi(date, time='0:0'):
    s_date = str(date).split('/')
    s_time = str(time).split(':')
    jalili_date = jdatetime.date(
        int(s_date[2]),
        int(s_date[1]),
        int(s_date[0]),
    )
    miladi_date = jalili_date.togregorian()
    res = datetime.datetime(
        miladi_date.year,
        miladi_date.month,
        miladi_date.day,
        int(s_time[0]),
        int(s_time[1]),
    )
    return res

from functools import wraps
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        res = func(*args, **kwargs)
        end = time.perf_counter_ns()
        total = end - start
        func_name = func.__name__
        print(f'{Colors.INFO}[INFO][{func_name}]: executing time: {(total)} nanosecond{Colors.RESET}')
        print(f'{Colors.INFO}[INFO][{func_name}]: executing time: {(total) / 1000} microsecond{Colors.RESET}')
        print(f'{Colors.INFO}[INFO][{func_name}]: executing time: {(total) / 1_000_000} milisecond{Colors.RESET}')
        return res
    return wrapper


def get_time_now():
    return datetime.datetime.now()
    return timezone.now() + datetime.timedelta(hours=3, minutes=30)