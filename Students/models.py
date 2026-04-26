from django.db import models
from Users.models import User
from Departments.models import Department

class Student(models.Model):
    # StudentID = models.AutoField(primary_key=True, verbose_name="شناسه دانشجو")

    UserKey = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="Userkey",
        verbose_name="شناسه کاربر"
    )

    DepartmentKey = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="DepartmentKey",
        verbose_name="شناسه دانشکده"
    )

    StudentNumber = models.CharField(max_length=20, unique=True, verbose_name="شماره دانشجویی")

    def __str__(self):
        return f"{self.UserKey.FirstName} {self.UserKey.LastName} ({self.StudentNumber})"

    class Meta:
        managed = False
        db_table = 'Students'