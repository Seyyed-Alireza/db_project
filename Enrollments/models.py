from django.db import models
from Students.models import Student
from Courses.models import Course

class Enrollment(models.Model):
    # EnrollmentID = models.AutoField(primary_key=True, verbose_name='شناسه ثبت‌نام')

    StudentKey = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='StudentKey',
        verbose_name='دانش‌آموز'
    )

    CourseKey = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        db_column='CourseKey',
        verbose_name='درس'
    )

    EnrolledAt = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت‌نام')

    Grade = models.CharField(max_length=5, blank=True, null=True, verbose_name='نمره نهایی')

    Status = models.CharField(max_length=20, default="active", verbose_name="وضعیت")

    def __str__(self):
        return f"{self.StudentKey.UserKey.FirstName} Enrolled {self.CourseKey.CourseName}"

    class Meta:
        managed = False
        db_table = 'Enrollments'
        unique_together = ('StudentKey', 'CourseKey')