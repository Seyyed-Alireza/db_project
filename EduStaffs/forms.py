from django import forms
from Courses.models import Course
from Enrollments.models import Enrollment
from Students.models import Student

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["CourseName", "CourseCode", "Units", "CoursePasswordHash"]
        widgets = {
            "CourseName": forms.TextInput(attrs={"class": "form-control"}),
            "CourseCode": forms.TextInput(attrs={"class": "form-control"}),
            "Units": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "CoursePasswordHash": forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        }
        labels = {
            "CourseName": "نام درس",
            "CourseCode": "کد درس",
            "Units": "تعداد واحد",
            "CoursePasswordHash": "رمز کلاس (اختیاری)",
        }

class EnrollStudentForm(forms.ModelForm):
    
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="انتخاب دانشجو",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Enrollment
        fields = []