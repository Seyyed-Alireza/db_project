from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files import File
import random
from Teachers.models import Teacher
from Students.models import Student
from Courses.models import Course
from Exams.models import Exam
from Departments.models import Department
from Users.models import User
from Enrollments.models import Enrollment
from main.views import get_time_now
from django.contrib.auth.models import User as SuperUser
from Questions.models import Question
from main.constant import EventType
import os
from FraudDetection.settings import MEDIA_ROOT

def random_datetime(start, end):
    start_day = int(start.day)
    end_day = int(end.day)
    
    start_ts = start.timestamp()
    end_ts   = end.timestamp()
    rand_ts  = random.uniform(start_ts, end_ts)
    rand_dt  = datetime.fromtimestamp(rand_ts)
    return rand_dt
    return timezone.make_aware(rand_dt, timezone.get_current_timezone())

class Command(BaseCommand):
    help = "Fill database with sample data"

    def handle(self, *args, **options):
        SuperUser.objects.all().delete()
        User.objects.all().delete()
        Department.objects.all().delete()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Enrollment.objects.all().delete()
        Question.objects.all().delete()
        Exam.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All previous data deleted successfully"))

        SuperUser.objects.create_superuser(
            username='admin',
            password='admin',
        )
        self.stdout.write(self.style.SUCCESS("Superuser created successfully"))

        USERNAMES = ["user1", "user2", "user3", "user4", "garden"]
        FIRST_NAMES = ["مرضیه", "صالح", "حسین", "آرش", "فرزانه"]
        LAST_NAMES = ["داوودآبادی فراهانی", "اعتمادی", "رحمانی", "عبدی", "غیور باغبانی"]
        ROLES = ["teacher", "teacher", "student"]
        DEPARTMENT_NAMES = ["کامپیوتر"]
        COURSE_NAMES = ["برنامه سازی پیشرفته", "داده ساختار و الگوریتم", "هوش مصنوعی"]
        EXAM_TITLES = ["پایان‌ترم", "میان‌ترم"]
        TOTAL_SCORES = [5, 8, 10, 20, 100]

        COURSE_COUNT = 3
        USER_COUNT = 8
        TEACHER_LIMIT = 2
        QUESTION_LIMIT = 3

        users = []
        for i in range(USER_COUNT):
            username = f"user{i}"
            role = "teacher"
            if (i > TEACHER_LIMIT):
                role = "student"
            users.append(
                User.objects.create(
                    Username=username,
                    FirstName=random.choice(FIRST_NAMES),
                    LastName=random.choice(LAST_NAMES),
                    PasswordHash=username,
                    Role=role,
                )
            )
        self.stdout.write(self.style.SUCCESS("Users created successfully"))

        departments = []
        for i in range(1):
            departments.append(
                Department.objects.create(
                    DepartmentName=random.choice(DEPARTMENT_NAMES),
                )
            )
        self.stdout.write(self.style.SUCCESS("Departments created successfully"))

        teachres = []
        students = []
        for user in users:
            if (user.Role == "teacher"):
                teachres.append(
                    Teacher.objects.create(
                        UserKey=user,
                        DepartmentKey=random.choice(departments),
                    )
                )
            elif (user.Role == "student"):
                students.append(
                    Student.objects.create(
                        StudentNumber=random.randint(100000000, 999999999),
                        UserKey=user,
                        DepartmentKey=random.choice(departments),
                    )
                )
        self.stdout.write(self.style.SUCCESS("Teachers and students created successfully"))

        courses = []
        for i in range(COURSE_COUNT):
            courses.append(
                Course.objects.create(
                    CourseName=random.choice(COURSE_NAMES),
                    CourseCode=random.randint(1000, 9999),
                    Units=random.randint(2, 3),
                    TeacherKey=random.choice(teachres),
                    DepartmentKey=random.choice(departments),
                )
            )
        self.stdout.write(self.style.SUCCESS("Courses created successfully"))

        enrollments = []
        for student in students:
            for course in random.sample(courses, k=random.randint(1, len(courses))):
                enrollments.append(
                    Enrollment.objects.create(
                        StudentKey=student,
                        CourseKey=course,
                        EnrolledAt=get_time_now(),
                    )
                )
        self.stdout.write(self.style.SUCCESS("Enrollments created successfully"))

        exams = []
        for course in courses:
            start_time = get_time_now() - timedelta(days=90)
            duration = random.randint(12, 120)
            exams.append(
                Exam.objects.create(
                    CourseKey=course,
                    TeacherKey=course.TeacherKey,
                    Title=random.choice(EXAM_TITLES),
                    StartTime=start_time,
                    EndTime=start_time+timedelta(hours=duration),
                    TotalScore=random.choice(TOTAL_SCORES),
                )
            )

            exams.append(
                Exam.objects.create(
                    CourseKey=course,
                    TeacherKey=course.TeacherKey,
                    Title=random.choice(EXAM_TITLES),
                    StartTime=get_time_now(),
                    EndTime=get_time_now()+timedelta(weeks=50),
                    TotalScore=random.choice(TOTAL_SCORES),
                )
            )

            start_time = get_time_now() + timedelta(days=60)
            duration = random.randint(12, 120)
            exams.append(
                Exam.objects.create(
                    CourseKey=course,
                    TeacherKey=course.TeacherKey,
                    Title=random.choice(EXAM_TITLES),
                    StartTime=start_time,
                    EndTime=start_time+timedelta(hours=duration),
                    TotalScore=random.choice(TOTAL_SCORES),
                )
            )

        self.stdout.write(self.style.SUCCESS("Exams created successfully"))

        questions = []
        for i in range(QUESTION_LIMIT):
            for exam in exams:
                question = Question.objects.create(
                    ExamKey=exam,
                    QuestionType=EventType.QUESTION_DESCRIPTIVE,
                    QuestionText='این متن سوال است',
                    Score=5,
                )
                question_image = os.path.join(MEDIA_ROOT, 'for_seed', f'default{i+1}.png')
                if os.path.exists(question_image):
                    with open(question_image, 'rb') as img_file:
                        question.QuestionImage.save(
                            f'question_{question.pk}.png',
                            File(img_file),
                            save=True
                        )
                    self.stdout.write(self.style.SUCCESS(f"✅ Image attached to question {question.pk} for exam {exam.pk}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Image file not found at {question_image}"))
                questions.append(question)

        self.stdout.write(self.style.SUCCESS(f"Questions created successfully"))

        self.stdout.write(self.style.SUCCESS("Done ✅"))