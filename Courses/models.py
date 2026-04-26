from django.db import models
from Departments.models import Department
from Teachers.models import Teacher
from Students.models import Student
from django.contrib.auth.hashers import make_password

class Course(models.Model):
    CourseID = models.AutoField(primary_key=True, verbose_name="شناسه درس")

    TeacherKey = models.ForeignKey(
        Teacher,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_column="TeacherKey",
        verbose_name="شناسه استاد"
    )
    
    DepartmentKey = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        db_column="DepartmentKey",
        verbose_name="شناسه دانشکده"
    )

    CourseName = models.CharField(max_length=100, verbose_name="نام درس")

    CourseCode = models.CharField(max_length=20, unique=True, verbose_name="کد درس")

    Units = models.PositiveSmallIntegerField(verbose_name="تعداد واحد")

    CoursePasswordHash = models.CharField(max_length=255, blank=True, null=True, verbose_name='هش رمز کلاس')

    def save(self, *args, **kwargs):
        if self.CoursePasswordHash:
            if not self.CoursePasswordHash.startswith('pbkdf2_'):
                self.CoursePasswordHash = make_password(self.CoursePasswordHash)
        super().save(*args, **kwargs)
    
    class Meta:
        managed = False
        db_table = 'Courses'
    
    def __str__(self):
        return f"{self.CourseCode} - {self.CourseName}"