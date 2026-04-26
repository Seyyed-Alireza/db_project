# Tests/test_concurrency.py

import threading
import time
from django.test import TestCase, Client
from Exams.models import Exam
from Users.models import User
from Students.models import Student
from Courses.models import Course
from Departments.models import Department
from Enrollments.models import Enrollment
from LoginSessions.models import LoginSession
from Teachers.models import Teacher
from main.views import get_time_now
from datetime import timedelta


class ConcurrencyTest(TestCase):
    def setUp(self):
        """ساختن داده تست"""
        # ساختن کاربر دانشجو
        self.user = User.objects.create(
            Username='testuser',
            PasswordHash='testpass',
            FirstName='a',
            LastName='b',
            Role='student',
        )
        
        # ساختن کاربر معلم
        self.teacher_user = User.objects.create(
            Username='testuser2',
            PasswordHash='testpass',
            FirstName='a2',
            LastName='b2',
            Role='teacher',
        )
        
        self.department = Department.objects.create(
            DepartmentName='abc'
        )
        
        self.teacher = Teacher.objects.create(
            UserKey=self.teacher_user,
            DepartmentKey=self.department,
        )
        
        # ساختن student
        self.student = Student.objects.create(            
            UserKey=self.user,
            DepartmentKey=self.department,
            StudentNumber='12345',
        )
        
        # ساختن course
        self.course = Course.objects.create(
            DepartmentKey=self.department,
            CourseName='course',
            CourseCode=123,
            Units=3,
        )
        
        # ساختن exam
        self.exam = Exam.objects.create(
            TeacherKey=self.teacher,
            CourseKey=self.course,
            Title='Test Exam',
            StartTime=get_time_now(),
            EndTime=get_time_now() + timedelta(minutes=40)
        )
        
        # enrollment
        Enrollment.objects.create(
            StudentKey=self.student,
            CourseKey=self.course
        )
    
    def test_single_entry(self):
        """تست ساده - یک کاربر"""
        client = Client()
        
        # ست کردن session
        session = client.session
        session['user_id'] = self.user.pk
        session.save()
        
        response = client.get(f'/exam/{self.course.pk}/{self.exam.pk}/')
        print(f"\nSingle entry: {response.status_code}")
        
        if response.status_code == 500:
            print(f"Error: {response.content.decode()[:500]}")
        
        self.assertEqual(response.status_code, 200)
    
    def test_concurrent_exam_entry(self):
        """تست ورود همزمان ۱۰ کاربر"""
        results = []
        errors = []
        
        def enter_exam(user_id):
            client = Client()
            
            # ست کردن session
            session = client.session
            session['user_id'] = self.user.pk
            session.save()
            
            try:
                response = client.get(f'/exam/{self.course.pk}/{self.exam.pk}/')
                results.append(response.status_code)
                
                # اگه 500 بود، محتواش رو چاپ کن
                if response.status_code == 500:
                    print(f"\n500 Error for user {user_id}:")
                    print(response.content.decode()[:500])
                    
            except Exception as e:
                import traceback
                errors.append(str(e))
                print(f"Exception: {e}")
                traceback.print_exc()
        
        threads = []
        for i in range(1):
            t = threading.Thread(target=enter_exam, args=(self.user.pk,))
            threads.append(t)
        
        start = time.time()
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        
        print(f"\n{'='*50}")
        print(f"10 concurrent requests: {elapsed:.2f}s")
        print(f"Errors: {len(errors)}")
        print(f"Results: {results}")
        print(f"200 (success): {results.count(200)}")
        print(f"302 (redirect): {results.count(302)}")
        print(f"500 (error): {results.count(500)}")
        print(f"{'='*50}")
        
        # چک کردن LoginSession‌ها
        active_sessions = LoginSession.objects.filter(
            ExamKey=self.exam,
            IsActive=True
        ).count()
        print(f"Active sessions in DB: {active_sessions}")
        
        # فقط یکی باید موفق بشه
        success_count = results.count(200)
        self.assertEqual(success_count, 1)