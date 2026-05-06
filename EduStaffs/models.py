from django.db import models
from Departments.models import Department
from Users.models import User

class EduStaff(models.Model):
    # EduID = models.AutoField(primary_key=True, verbose_name="شناسه آموزش")

    UserKey = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="Userkey",
        verbose_name="شناسه کاربر"
    )

    DepartmentKey = models.OneToOneField(
        Department,
        on_delete=models.CASCADE,
        db_column="DepartmentKey",
        verbose_name="شناسه دانشکده"
    )

    def __str__(self):
        return f"آموزش دانشکده {self.DepartmentKey.DepartmentName}"
    
    class Meta:
        managed = False
        db_table = "EduStaffs"