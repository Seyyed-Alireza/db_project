from django.db import models
from Exams.models import Exam
from Students.models import Student

class ExamResult(models.Model):
    # ResultID = models.AutoField(primary_key=True, verbose_name="شناسه نتیجه")

    ExamKey = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        db_column="ExamKey",
        verbose_name="شناسه امتحان"
    )

    StudentKey = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column="StudentKey",
        verbose_name="شناسه دانشجو"
    )

    TotalScore = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="نمره کسب شده")

    Status = models.BooleanField(default=True, verbose_name="وضعیت قبولی")

    Grade = models.CharField(max_length=20, verbose_name="سطج بندی نمره")

    CalculatedAt = models.DateTimeField(auto_now_add=True, verbose_name="زمان محاسبه")

    def __str__(self):
        return f"Result calculated at {self.CalculatedAt.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'ExamResults'
        unique_together = ('ExamKey', 'StudentKey')