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
from EduStaffs.models import EduStaff
from LoginSessions.models import LoginSession
from ExamResults.models import ExamResult
from IPAddressLogs.models import IPAddressLog
from FraudFlags.models import FraudFlag
from QuestionOptions.models import QuestionOption
from BehavioralMetrics.models import BehavioralMetric
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
        EduStaff.objects.all().delete()
        LoginSession.objects.all().delete()
        ExamResult.objects.all().delete()
        IPAddressLog.objects.all().delete()
        FraudFlag.objects.all().delete()
        QuestionOption.objects.all().delete()
        BehavioralMetric.objects.all().delete()
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
        DEPARTMENT_NAMES = ["کامپیوتر", "برق", "مکانیک", "معماری", "فیزیک"]
        COURSE_NAMES = ["برنامه سازی پیشرفته", "داده ساختار و الگوریتم", "هوش مصنوعی", "مدار  منطقی", "ریاضیات گسسته", "فیزیک 1", "فیزیک 2", "جبر خطی"]
        EXAM_TITLES = ["پایان‌ترم", "میان‌ترم"]
        TOTAL_SCORES = [5, 8, 10, 20, 100]

        COURSE_COUNT = 12
        USER_COUNT = 50
        TEACHER_LIMIT = 10
        STAFF_LIMIT = TEACHER_LIMIT + 12
        QUESTION_LIMIT = 3
        DEPARTMENT_COUNT = 12

        users = []
        for i in range(USER_COUNT):
            username = f"user{i+1}"
            role = "teacher"
            if (i < TEACHER_LIMIT):
                role = "teacher"
            elif (i < STAFF_LIMIT):
                role = "staff"
            else:
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
        for i in range(DEPARTMENT_COUNT):
            departments.append(
                Department.objects.create(
                    DepartmentName=random.choice(DEPARTMENT_NAMES),
                )
            )
        self.stdout.write(self.style.SUCCESS("Departments created successfully"))

        teachres = []
        students = []
        staffs = []
        for user in users:
            if (user.Role == "student"):
                students.append(
                    Student.objects.create(
                        StudentNumber=random.randint(100000000, 999999999),
                        UserKey=user,
                        DepartmentKey=random.choice(departments),
                    )
                )
            elif (user.Role == "teacher"):
                teachres.append(
                    Teacher.objects.create(
                        UserKey=user,
                        DepartmentKey=random.choice(departments),
                    )
                )
            elif (user.Role == "staff"):
                staffs.append(
                    EduStaff.objects.create(
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
                    # self.stdout.write(self.style.SUCCESS(f"✅ Image attached to question {question.pk} for exam {exam.pk}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Image file not found at {question_image}"))
                questions.append(question)

        self.stdout.write(self.style.SUCCESS(f"Questions created successfully"))

        login_sessions = []
        for i in range(20):
            login_sessions.append(
                LoginSession.objects.create(
                    StudentKey=random.choice(students),
                    ExamKey=random.choice(exams),
                    LoginTime=get_time_now()-timedelta(hours=random.randint(24, 47)),
                    LogoutTime=get_time_now()-timedelta(hours=random.randint(48, 72)),
                    IsActive=False,
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Login sessions created successfully"))

        behaviorals = []
        for question in questions:
            time_spent=random.randint(200, 1000)
            behaviorals.append(
                BehavioralMetric.objects.create(
                    SessionKey=random.choice(login_sessions),
                    QuestionKey=question,
                    TotalTimeSpent=time_spent,
                    TabSwitchCount=random.choice([0, 0, 0, 0, 0, 0, 1, 2, 3, 4]),
                    CopyPasteCount=random.choice([0, 0, 0, 0, 0, 0, 1, 2, 3, 4]),
                    IdleTime=time_spent-20,
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Behavioral metrics created successfully"))

        exam_results = []
        for exam in exams:
            exam_results.append(
                ExamResult.objects.create(
                    ExamKey=exam,
                    StudentKey=random.choice(students),
                    TotalScore=random.randint(10, 20),
                    Grade=random.choice(['A', 'B', 'C']),
                    CalculatedAt=get_time_now(),
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Exam results created successfully"))
        
        fraud_flags= []
        reasons = [f'reason_{i}' for i in range(20)]
        severities = [f'severity_{i}' for i in range(10)]
        flags = [f'flag_{i}' for i in range(5)]
        statuses = [f'status_{i}' for i in range(10)]
        for question in questions:
            fraud_flags.append(
                FraudFlag.objects.create(
                    SessionKey=random.choice(login_sessions),
                    QuestionKey=question,
                    Reason=random.choice(reasons),
                    RiskScore=random.randint(0, 10),
                    Severity=random.choice(severities),
                    FlagType=random.choice(flags),
                    Status=random.choice(statuses),
                    GeneratedAt=get_time_now(),
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Fraud flags created successfully"))
        
        IPs = [f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}']
        locations = [f'location_{i}' for i in range(10)]
        IP_logs = []
        for i in range(20):
            IP_logs.append(
                IPAddressLog.objects.create(
                    SessionKey=random.choice(login_sessions),
                    IPAddress=random.choice(IPs),
                    LogTime=get_time_now()-timedelta(hours=random.randint(48, 72)),
                    Location=random.choice(locations),
                )
            )
        self.stdout.write(self.style.SUCCESS(f"IP logs created successfully"))

        option_texts = [f'option_{i}' for i in range(100)]
        option_lables = [f'label_{i}' for i in range(1, 5)]
        options = []
        for question in questions:
            options.append(
                QuestionOption.objects.create(
                    QuestionKey=question,
                    OptionText=random.choice(option_texts),
                    OptionLabel=random.choice(option_lables),
                    IsCorrect=random.choice([True, True, True, False]),
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Question options created successfully"))

        self.stdout.write(self.style.SUCCESS("Done ✅"))