from django.db import models
from Exams.models import Exam
from Students.models import Student
from decimal import Decimal
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

    TotalScore = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=Decimal("0.00"),
    verbose_name="نمره کل"
    )

    Status = models.BooleanField(default=True, verbose_name="وضعیت قبولی")

    Grade = models.CharField(max_length=20, verbose_name="سطج بندی نمره")

    CalculatedAt = models.DateTimeField(auto_now_add=True, verbose_name="زمان محاسبه")

    def __str__(self):
        return f"Result calculated at {self.CalculatedAt.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'ExamResults'
        unique_together = ('ExamKey', 'StudentKey')