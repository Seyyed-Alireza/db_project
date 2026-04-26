from django.db import models
from Questions.models import Question
from Students.models import Student
from QuestionOptions.models import QuestionOption

class Answer(models.Model):
    # AnswerID = models.AutoField(primary_key=True, verbose_name="شناسه پاسخ")
    
    QuestionKey = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        db_column="QuestionKey",
        verbose_name="شناسه سوال"
    )
    
    StudentKey = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column="StudentKey",
        verbose_name="شناسه دانشجو"
    )
    
    SelectedOptionKey = models.ForeignKey(
        QuestionOption,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="SelectedOptionKey",
        verbose_name="شناسه گزینه انتخاب شده"
    )
    
    AnswerText = models.TextField(blank=True, null=True, verbose_name="متن پاسخ")
    
    IsCorrect = models.BooleanField(default=False, blank=True, null=True, verbose_name="آیا صحیح است؟")
    
    AnswerFile = models.FileField(upload_to='answer_files/', blank=True, null=True, verbose_name="تصویر پاسخ")

    IsGraded = models.BooleanField(default=False, verbose_name="وضعیت تصحیح")

    GivenScore = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="نمره اخذ شده")

    SubmittedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پاسخ دانشجو {self.student_id} به سوال {self.question_id}"

    class Meta:
        managed = False
        db_table = 'Answers'
        unique_together = ('StudentKey', 'QuestionKey')