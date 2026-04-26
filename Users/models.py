from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    UserID = models.AutoField(primary_key=True, verbose_name='شناسه کاربر')

    Username = models.CharField(max_length=150, unique=True, verbose_name='نام کاربری')

    FirstName = models.CharField(max_length=100, verbose_name='نام')

    LastName = models.CharField(max_length=100, verbose_name='نام خانوادگی')

    PasswordHash = models.CharField(max_length=255, verbose_name='رمز عبور (هش شده)')

    def save(self, *args, **kwargs):
        if not self.PasswordHash.startswith('pbkdf2_'):
            self.PasswordHash = make_password(self.PasswordHash)
        super().save(*args, **kwargs)

    Role = models.CharField(max_length=50, verbose_name='نقش کاربر')

    Email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='ایمیل')

    PhoneNumber = models.CharField(max_length=15, blank=True, null=True, verbose_name='شماره تلفن')

    CreatedAt   = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    IsLoggedIn  = models.BooleanField(default=False, verbose_name='وضعیت ورود')

    def __str__(self):
        return f'{self.Username} ({self.FirstName} {self.LastName})'

    class Meta:
        managed = False
        db_table = 'Users'