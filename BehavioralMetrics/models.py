from django.db import models
from LoginSessions.models import LoginSession
from Questions.models import Question

class BehavioralMetric(models.Model):
    # MetricID = models.AutoField(primary_key=True, verbose_name="شناسه شاخص")

    SessionKey = models.ForeignKey(
        LoginSession,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="SessionKey",
        verbose_name="شناسه جلسه"
    )

    QuestionKey = models.ForeignKey(
        Question,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        db_column="QuestionKey",
        verbose_name="شناسه سوال"
    )

    TotalTimeSpent = models.PositiveIntegerField(default=0, verbose_name="مجموع زمان صرف شده")

    VisitCount = models.PositiveSmallIntegerField(default=1, verbose_name="تعداد بازدید")

    TabSwitchCount = models.PositiveSmallIntegerField(default=0, verbose_name="تعداد تغییر تب")

    CopyPasteCount = models.PositiveSmallIntegerField(default=0, verbose_name="نعداد کپی پیست")

    IdleTime = models.IntegerField(default=0, verbose_name="زمان بی فعالی")

    def __str__(self):
        return f"شاخص های رفتاری مربوط به {self.SessionID.SessionID}"
    
    class Meta:
        managed = False
        db_table = 'BehavioralMetrics'
        unique_together = ('SessionKey', 'QuestionKey')