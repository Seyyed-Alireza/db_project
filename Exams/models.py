from django.db import models
from Courses.models import Course
from Teachers.models import Teacher
from django.utils import timezone


class Exam(models.Model):
    ExamID = models.AutoField(primary_key=True, verbose_name="شناسه امتحان")

    CourseKey = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        db_column='CourseKey',
        verbose_name="شناسه درس"
    )

    TeacherKey = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        db_column='TeacherKey',
        verbose_name="شناسه استاد"
    )

    Title = models.CharField(max_length=200, verbose_name="عنوان امتحان")

    StartTime = models.DateTimeField(verbose_name="زمان شروع")
    
    EndTime = models.DateTimeField(verbose_name="زمان پایان")

    Duration = models.PositiveIntegerField(blank=True, null=True, verbose_name="مدت زمان")

    def save(self, *args, **kwargs):
        if not self.Duration:
            duration = self.EndTime - self.StartTime
            minutes = max(duration.total_seconds() // 60, 0)
            self.Duration = minutes

        super().save(*args, **kwargs)

    Description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    
    TotalScore = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="نمره کل", 
        blank=True, 
        null=True,
        default='0',
    )

    def __str__(self):
        return f"{self.Title} - {self.CourseKey.CourseName} - {self.StartTime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'Exams'