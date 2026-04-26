from django import forms
from .models import Exam
import datetime
import jdatetime
from main.views import to_miladi

def validate_date(date_input):
    date = str(date_input).strip().split('/')
    if (len(date) != 3):
        return False
    try:
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
    except:
        return False
    is_leap = year % 33 in [1, 5, 9, 13, 17, 22, 26, 30]

    if (year < 1405):
        return False
    if (1 <= month and month <= 6):
        if (day > 31 or day < 0):
            return False
    elif (7 <= month and month <= 11):
        if (day > 30 or day < 0):
            return False
    elif (month == 12):
        if (is_leap):
            if (day > 30 or day < 0):
                return False
        else:
            if (day > 29 or day < 0):
                return False
    else:
        return False        

    return True
    
def validate_time(time_input):
    time = str(time_input).strip().split(':')
    if (len(time) != 2):
        return False
    try:
        hour = int(time[0])
        minute = int(time[1])
    except:
        return False
    
    if not(0 <= minute <= 59 and 0 <= hour <= 23):
        return False
    
    return True


class ExamForm(forms.Form):
    
    title = forms.CharField(
        label='عنوان آزمون',
        widget=forms.TextInput(attrs={
            'placeholder': 'عنوان آزمون',
            'autofocus': 'true',
            'class': 'form-input',
            }
        ),
        error_messages={
            'invalid': 'نامعتبر',
            'required': 'وارد کردن عنوان الزامی است.',
        },
    )

    description = forms.CharField(
        label='توضیحات (اختیاری)',
        required=False,  # چون گفتی اختیاری
        widget=forms.Textarea(attrs={
            'placeholder': 'توضیحات',
            'rows': 3,
            'cols': 50,
            'class': 'form-input',
        }),
    )

    start_date = forms.CharField(
        label='تاریخ شروع (سال/ماه/روز)',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 1/1/1405',
            'class': 'form-input dir-ltr',
            }
        ),
        error_messages={
            'invalid': 'نامعتبر',
            'required': 'وارد کردن تاریخ شروع الزامی است.',
        },
    )

    start_time = forms.CharField(
        label='زمان شروع (دقیقه:ساعت)',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 20:30',
            'class': 'form-input dir-ltr',
            }
        ),
        error_messages={
            'invalid': 'نامعتبر',
            'required': 'وارد کردن زمان شروع الزامی است.',
        },
    )

    end_date = forms.CharField(
        label='تاریخ پایان (سال/ماه/روز)',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 1/1/1405',
            'class': 'form-input dir-ltr',
            }
        ),
        error_messages={
            'invalid': 'نامعتبر',
            'required': 'وارد کردن تاریخ پایان الزامی است.',
        },
    )

    end_time = forms.CharField(
        label='زمان پایان (دقیقه:ساعت)',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثال: 21:30',
            'class': 'form-input dir-ltr',
            }
        ),
        error_messages={
            'invalid': 'نامعتبر',
            'required': 'وارد کردن زمان پایان الزامی است.',
        },
    )

    def clean_start_date(self):
        s_day = self.cleaned_data.get('start_date')
        if not(validate_date(s_day)):
            raise forms.ValidationError('تاریخ شروع نامعتبر است.')

        return s_day
        
    def clean_start_time(self):
        s_time = self.cleaned_data.get('start_time')
        if not(validate_time(s_time)):
            raise forms.ValidationError('زمان شروع نامعتبر است.')
        
        return s_time
        
    def clean_end_date(self):
        e_day = self.cleaned_data.get('end_date')
        if not(validate_date(e_day)):
            raise forms.ValidationError('تاریخ پایان نامعتبر است.')
        
        return e_day
        
    def clean_end_time(self):
        e_time = self.cleaned_data.get('end_time')
        if not(validate_time(e_time)):
            raise forms.ValidationError('زمان پایان نامعتبر است.')
        
        return e_time

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        if all([start_date, start_time, end_date, end_time]):
            start_datetime = to_miladi(start_date, start_time)
            end_datetime = to_miladi(end_date, end_time)
            if (end_datetime < start_datetime):
                raise forms.ValidationError('زمان پایان آزمون نمی‌تواند قبل از شروع باشد.')

        return cleaned_data
    
    