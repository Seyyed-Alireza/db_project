from django import forms
from django.contrib.auth.hashers import check_password
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='نام کاربری',
        widget=forms.TextInput(attrs={
            'placeholder': 'نام کاربری',
            'autofocus': 'true',
            }
        ),
        error_messages={
            'required': 'وارد کردن نام کاربری الزامی است.',
        },
    )
    password = forms.CharField(
        max_length=255,
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
        error_messages={
            'required': 'وارد کردن رمز عبور الزامی است.',
        },
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            return cleaned_data

        try:
            user = User.objects.get(Username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('نام کاربری یافت نشد.')

        if not check_password(password, user.PasswordHash):
            raise forms.ValidationError('رمز عبور نادرست.')

        cleaned_data['user'] = user
        return cleaned_data