from django.db import models
from LoginSessions.models import LoginSession
from Questions.models import Question

class FraudFlag(models.Model):
    FlagID = models.AutoField(primary_key=True, verbose_name="شناسه پرچم")

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
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="QuestionKey",
        verbose_name="شناسه سوال"
    )

    Reason = models.TextField(blank=True, null=True, verbose_name="دلیل")
    RiskScore = models.PositiveSmallIntegerField(default=0, verbose_name="امتیاز ریسک")

    Severity = models.CharField(max_length=100, verbose_name="شدت تخلف")

    FlagType = models.TextField(blank=True, null=True, verbose_name="نوع تخلف")

    Status = models.CharField(max_length=100, verbose_name="وضعیت نهایی")

    GeneratedAt = models.DateTimeField(auto_now_add=True, verbose_name="زمان تولید")

    def __str__(self):
        return f"Fraud with {self.RiskScore} risk score at {self.GeneratedAt.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'FraudFlags'