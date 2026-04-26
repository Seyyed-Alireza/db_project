from django.db import models
from LoginSessions.models import LoginSession
from Questions.models import Question

class TabSwitchLog(models.Model):
    LogID = models.AutoField(primary_key=True, verbose_name="شناسه لاگ")

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

    EventTime = models.DateTimeField(auto_now_add=True, verbose_name="زمان رویداد")

    EventType = models.SmallIntegerField(blank=True, null=True, verbose_name="نوع رویداد")

    Duration = models.DecimalField(
        max_digits=65,
        decimal_places=2,
        blank=True, null=True, verbose_name="مدت زمان"
    )

    def __str__(self):
        return f"Browser tab changed at {self.EventTime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'TabSwitchLogs'
    
