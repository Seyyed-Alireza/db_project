from django.db import models
from LoginSessions.models import LoginSession
from Questions.models import Question

class QuestionViewLog(models.Model):
    # ViewLogID = models.AutoField(primary_key=True, verbose_name="شناسه لاگ")

    SessionKey = models.ForeignKey(
        LoginSession,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="SessionKey",
        verbose_name="شناسه جلسه"
    )

    QuestionKey = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="QuestionKey",
        verbose_name="شناسه سوال"
    )

    ViewStartTime = models.DateTimeField(blank=True, null=True, verbose_name="زمان شروع بازدید")

    ViewEndTime = models.DateTimeField(blank=True, null=True, verbose_name="زمان پایان بازدید")

    Duration = models.PositiveIntegerField(blank=True, null=True, verbose_name="مدت زمان")

    def __str__(self):
        return f"Question {self.QuestionID} viewed at {self.ViewStartTime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'QuestionViewLogs'
        unique_together = ('SessionKey', 'QuestionKey')