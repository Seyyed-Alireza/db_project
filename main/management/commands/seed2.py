from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
import random
from Teachers.models import Teacher
from Students.models import Student
from Courses.models import Course
from Exams.models import Exam
from Departments.models import Department
from Users.models import User
from Enrollments.models import Enrollment
from main.views import get_time_now
from Answers.models import Answer
from Enrollments.models import Enrollment

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
        Enrollment.objects.filter(
            StudentKey_id=20,
            CourseKey_id=9,
        ).delete()
        Enrollment.objects.create(
            StudentKey_id=20,
            CourseKey_id=9,
            EnrolledAt=get_time_now(),
        )
        self.stdout.write(self.style.SUCCESS("Enrollment created successfully"))

        self.stdout.write(self.style.SUCCESS("Done ✅"))