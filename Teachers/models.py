from django.db import models
from Users.models import User
from Departments.models import Department

class Teacher(models.Model):
    # TeacherId = models.AutoField(primary_key=True, verbose_name="شناسه استاد")
    UserKey = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="UserKey",
        verbose_name="شناسه کاربر"
    )

    DepartmentKey = models.ForeignKey(
        Department,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_column="DepartmentKey",
        verbose_name="شناسه دانشکده"
    )

    def __str__(self):
        return f"{self.UserKey.FirstName} {self.UserKey.LastName}"

    class Meta:
        managed = False
        db_table = 'Teachers'