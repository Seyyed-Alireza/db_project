from django.db import models

class Department(models.Model):
    DepartmentID = models.AutoField(primary_key=True, verbose_name="شناسه دانشکده")

    DepartmentName = models.CharField(max_length=100, verbose_name="نام دانشکده")

    Location = models.CharField(max_length=200, verbose_name="موقعیت", blank=True, null=True)
    
    Phone = models.CharField(max_length=20, verbose_name="تلفن", blank=True, null=True)

    def __str__(self):
        return self.DepartmentName
    
    class Meta:
        managed = False
        db_table = 'Departments'