from django.db import models
from Questions.models import Question

class QuestionOption(models.Model):

    OptionID = models.AutoField(primary_key=True, verbose_name="شناسه گزینه")

    QuestionKey = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        db_column="QuestionKey",
        verbose_name="شناسه سوال"
    )

    OptionText = models.TextField(blank=True, null=True, verbose_name="متن گزینه")

    OptionLabel = models.CharField(max_length=100, verbose_name="برچسب گزینه")

    IsCorrect = models.BooleanField(default=False, verbose_name="صحیح است")

    def __str__(self):
        return f"گزینه با عنوان {self.OptionLabel}"

    class Meta:
        managed = False
        db_table = 'QuestionOptions'