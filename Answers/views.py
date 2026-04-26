import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.text import slugify
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from FraudDetection.settings import MEDIA_ROOT
from .models import Answer
from Questions.models import Question
from main.constant import EventType
from .forms import DescriptiveAnswerForm, MultipleChoiceAnswerForm
from main.views import get_time_now
import time


def save_answer_d(request, question_id):
    if (request.method == 'POST'):
        exam_id = request.session.get('exam_id', None)
        std_id = request.session.get('user_id', None)
        if not(all([exam_id, std_id])):
            return JsonResponse({
                'success': False,
                'message': 'Unknown exam'
            })
        try:
            Question.objects.get(QuestionID=question_id, ExamKey_id=exam_id, QuestionType=EventType.QUESTION_DESCRIPTIVE)
        except ObjectDoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'question not found'
            })
        form = DescriptiveAnswerForm(request.POST, request.FILES)
        if not(form.is_valid()):
            return JsonResponse({
                'success': False,
                'message': form.errors
            }, status=400)
        
        answer_text = form.cleaned_data.get('answer_text')
        uploaded_file = form.cleaned_data.get('answer_file')
        file_path = None
        if uploaded_file:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT AnswerFile FROM answers 
                    WHERE QuestionKey = %s AND StudentKey = %s
                """, [question_id, std_id])
                row = cursor.fetchone()
                if row and row[0]:
                    old_file_path = os.path.join(MEDIA_ROOT, row[0])
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                    
            ext = os.path.splitext(uploaded_file.name)[1]
            original_name = os.path.splitext(uploaded_file.name)[0]
            safe_name = slugify(original_name)[:30]
            filename = f"answer_files/{exam_id}/S{std_id}_Q{question_id}_{safe_name}{ext}"
            saved_path = default_storage.save(filename, ContentFile(uploaded_file.read()))
            file_path = saved_path
            # answer_text = form.cleaned_data['answer_text']
        if (file_path):
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO answers (
                        QuestionKey,
                        StudentKey,
                        AnswerText,
                        SubmittedAt,
                        AnswerFile
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        AnswerText = VALUES(AnswerText),
                        SubmittedAt = Values(SubmittedAt),
                        AnswerFile = VALUES(AnswerFile)
                """, [question_id, std_id, answer_text, get_time_now(), file_path])
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO answers (
                        QuestionKey,
                        StudentKey,
                        AnswerText,
                        SubmittedAt
                    )
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        AnswerText = VALUES(AnswerText),
                        SubmittedAt = Values(SubmittedAt)
                """, [question_id, std_id, answer_text, get_time_now()])
        # answer, created = Answer.objects.update_or_create(
        #     QuestionKey_id=question_id,
        #     StudentKey_id=std_id,
        #     defaults={
        #         'AnswerText': form.cleaned_data.get('answer_text'),
        #         'SubmittedAt': get_time_now(),
        #         'SelectedOptionKey': None,
        #         'IsCorrect': False,
        #     }
        # )
        
        # if form.cleaned_data.get('AnswerFile'):
        #     answer = Answer.objects.get(QuestionKey_id=question_id, StudentKey_id=std_id)
        #     answer.AnswerFile = form.cleaned_data['AnswerFile']
        #     answer.save(update_fields=['AnswerFile'])

        return JsonResponse({
            'success': True,
            'message': 'پاسخ با موفقیت ذخیره شد.'
        })
    return JsonResponse({}, status=404)

