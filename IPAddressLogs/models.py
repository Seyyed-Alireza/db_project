from django.db import models
from LoginSessions.models import LoginSession

class IPAddressLog(models.Model):
    LogID = models.AutoField(primary_key=True, verbose_name="شناسه لاگ")

    SessionKey = models.ForeignKey(
        LoginSession,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="SessionKey",
        verbose_name="شناسه جلسه"
    )

    IPAddress = models.GenericIPAddressField(blank=True, null=True, verbose_name="آدرس IP")

    LogTime = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    Location = models.CharField(max_length=200, blank=True, null=True, verbose_name="موقعیت مکانی")

    def __str__(self):
        return f"IP address changed at {self.ViewStartTime.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        managed = False
        db_table = 'IPAddressLogs'