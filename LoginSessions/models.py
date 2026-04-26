from django.db import models
from Students.models import Student
from Exams.models import Exam

class LoginSession(models.Model):
    SessionID = models.AutoField(primary_key=True, verbose_name="شناسه جلسه")

    StudentKey = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column="StudentKey",
        verbose_name="شناسه دانشجو"
    )

    ExamKey = models.ForeignKey(
        Exam,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="ExamKey",
        verbose_name="شناسه امتحان"
    )

    LoginTime = models.DateTimeField(blank=True, null=True, verbose_name="زمان ورود")

    LogoutTime = models.DateTimeField(blank=True, null=True, verbose_name="زمان خروج")

    IsActive = models.BooleanField(default=True, verbose_name="وضعیت فعال")

    def __str__(self):
        return f"{self.StudentKey.StudentId}"

    class Meta:
        managed = False
        db_table = 'LoginSessions'