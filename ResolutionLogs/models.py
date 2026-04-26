from django.db import models
from LoginSessions.models import LoginSession

class ResolutionLog(models.Model):
    LogID = models.AutoField(primary_key=True, verbose_name="شناسه لاگ")

    SessionKey = models.ForeignKey(
        LoginSession,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="SessionKey",
        verbose_name="شناسه جلسه"
    )

    ScreenWidth = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="عرض کل صفحه نمایش")

    ScreenHeight = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="ارتفاع کل صفحه نمایش")

    WindowWidth = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="عرض پنجره مررگر")

    WindowHeight = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="ارتفاع پنجره مررگر")

    ChangeTime = models.DateTimeField(auto_now_add=True, verbose_name="زمان تغییر")

    def __str__(self):
        return f"Resolution changed at {self.ChangeTime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'ResolutionLogs'