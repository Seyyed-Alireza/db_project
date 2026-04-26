from django import forms
from QuestionOptions.models import QuestionOption

class MultipleChoiceAnswerForm(forms.Form):
    
    SelectedOptionKey = forms.ModelChoiceField(
        queryset=QuestionOption.objects.none(),
        label="گزینه مورد نظر",
        widget=forms.RadioSelect(attrs={
            'class': 'option-radio'
        }),
        error_messages={
            'required': 'لطفاً یک گزینه را انتخاب کنید.'
        }
    )
    
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        
        if self.question:
            # ⭐ فقط گزینه‌های همین سوال
            self.fields['SelectedOptionKey'].queryset = QuestionOption.objects.filter(
                QuestionKey=self.question
            )
            # برای نمایش بهتر
            self.fields['SelectedOptionKey'].label_from_instance = self._get_option_label
    
    def _get_option_label(self, obj):
        """نمایش گزینه به صورت: الف) متن گزینه"""
        return f"{obj.OptionLabel}) {obj.OptionText}"
    
    def clean_SelectedOptionKey(self):
        option = self.cleaned_data.get('SelectedOptionKey')
        
        # بررسی امنیتی: آیا گزینه واقعاً متعلق به این سوال است؟
        if option and option.QuestionKey_id != self.question.QuestionID:
            raise forms.ValidationError('گزینه انتخاب شده معتبر نیست.')
        
        return option
    
    def save(self, question, student):
        """ذخیره پاسخ تستی"""
        from Answers.models import Answer
        
        selected_option = self.cleaned_data['SelectedOptionKey']
        
        answer, created = Answer.objects.update_or_create(
            QuestionKey=question,
            StudentKey=student,
            defaults={
                'SelectedOptionKey': selected_option,
                'IsCorrect': selected_option.IsCorrect,
                'answer_text': None,  # صراحتاً NULL
                'answer_file': None,  # صراحتاً NULL
            }
        )
        return answer
    


# forms.py
from django import forms
from django.core.exceptions import ValidationError
import os

class DescriptiveAnswerForm(forms.Form):
    answer_text = forms.CharField(
        required=False,
        label="پاسخ تشریحی",
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 6,
            'placeholder': 'پاسخ خود را بنویسید...',
        })
    )
    
    answer_file = forms.FileField(
        required=False,
        label="فایل پاسخ (اختیاری)",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png,.gif,.pdf,.zip'
        }),
        help_text="فرمت‌های مجاز: JPG, PNG, PDF, ZIP (حداکثر ۱۰ مگابایت)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        answer_text = cleaned_data.get('answer_text')
        answer_file = cleaned_data.get('answer_file')
        
        if not answer_text and not answer_file:
            raise ValidationError(
                'برای سوال تشریحی باید حداقل پاسخ متنی یا فایل را وارد کنید.'
            )
        
        return cleaned_data
    
    def clean_answer_file(self):
        answer_file = self.cleaned_data.get('answer_file')
        
        if answer_file:
            max_size = 10 * 1024 * 1024
            if answer_file.size > max_size:
                raise ValidationError('حجم فایل نباید بیشتر از ۱۰ مگابایت باشد.')
            
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip']
            ext = os.path.splitext(answer_file.name)[1].lower()
            
            if ext not in allowed_extensions:
                raise ValidationError(
                    f'فرمت فایل مجاز نیست. فرمت‌های مجاز: {", ".join(allowed_extensions)}'
                )
            
            if not self._validate_file_content(answer_file, ext):
                raise ValidationError('محتوای فایل معتبر نیست.')
        
        return answer_file
    
    def _validate_file_content(self, file, ext):
        header = file.read(4)
        file.seek(0)
        
        magic_numbers = {
            '.jpg': [b'\xff\xd8\xff'],
            '.jpeg': [b'\xff\xd8\xff'],
            '.png': [b'\x89PNG'],
            '.gif': [b'GIF8'],
            '.pdf': [b'%PDF'],
            '.zip': [b'PK\x03\x04'],
        }
        
        if ext in magic_numbers:
            return any(header.startswith(magic) for magic in magic_numbers[ext])
        
        return True
    
    # def save(self, question, student):
    #     from Answers.models import Answer
        
    #     answer, created = Answer.objects.update_or_create(
    #         QuestionKey=question,
    #         StudentKey=student,
    #         defaults={
    #             'answer_text': self.cleaned_data.get('answer_text'),
    #             'SelectedOptionKey': None,  # صراحتاً NULL
    #             'IsCorrect': False,  # سوال تشریحی باید بعداً تصحیح شود
    #         }
    #     )
        
    #     if self.cleaned_data.get('answer_file'):
    #         answer.answer_file = self.cleaned_data['answer_file']
    #         answer.save()
        
    #     return answer