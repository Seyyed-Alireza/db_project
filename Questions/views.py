from django.shortcuts import render
from django.db import connection
from django.template.loader import render_to_string
from main.constant import EventType, Colors
from .models import Question
from Answers.forms import DescriptiveAnswerForm, MultipleChoiceAnswerForm
from LoginSessions.models import LoginSession
from Exams.models import Exam
from Answers.models import Answer
from django.http import JsonResponse
import json
import base64
from main.views import timer

def validate_for_question(request, order, navigate=True):
    if (request.method == 'POST'):
        if not(order):
            return False, JsonResponse({
                'success': False,
                'error': 'not_in_exam'
            })
        if not(navigate):
            try:
                data = json.loads(request.body)
                order = data.get('order')
            except json.JSONDecodeError:
                return False, JsonResponse({
                    'success': False,
                    'error': 'invalid_json'
                }, status=400)
            if not(order):
                return False, JsonResponse({
                    'success': False,
                    'error': 'order_required'
                }, status=400)
        # data = json.loads(request.body)
        # order = data.get('order')
        exam_id = request.session.get('exam_id')
        try:
            login_session = LoginSession.objects.get(
                StudentKey_id=request.session.get('user_id'),
                ExamKey_id=exam_id,
                IsActive=True,
            )
        except LoginSession.DoesNotExist:
            return False, JsonResponse({
                'success': False,
                'error': 'invalid_session'
            }, status=403)
        q = Question.objects.get(ExamKey_id=exam_id, Order=order)
        return True, q
    else:
        return False, JsonResponse({
            'success': False,
            'error': 'no_view'
        }, status=405)

def get_question(request, q):
    image_base64 = None
    if q.QuestionImage:
        with open(q.QuestionImage.path, 'rb') as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    existing_file = None
    if (q.QuestionType == EventType.QUESTION_DESCRIPTIVE):
        initial = {}
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT AnswerText, AnswerFile 
                FROM Answers 
                WHERE QuestionKey = %s AND StudentKey = %s
            """, [q.pk, request.session.get('user_id')])
            row = cursor.fetchone()
            if row:
                initial['answer_text'] = row[0]
                if row[1]:
                    existing_file = {
                        'name': row[1].split('_')[-1],
                        'url': f"/media/{row[1]}"
                    }
        form = DescriptiveAnswerForm(initial=initial)
        template_partial = 'Questions/descriptive_question.html'
            

    request.session['question_order'] = q.Order
    question = {
        'id': q.pk,
        'type': 'd' if q.QuestionType == EventType.QUESTION_DESCRIPTIVE else 'm',
        'text': q.QuestionText,
        'image': f'data:image/png;base64,{image_base64}' if image_base64 else None,
        'score': q.Score,
        'order': q.Order,
    }
    context = {
        'question': question,
        'form': form,
        'existing_file': existing_file,
        'first_question': q.Order == 1,
        'last_question': not Question.objects.filter(ExamKey_id=q.ExamKey_id, QuestionID__gt=q.pk).exists()
    }

    return render_to_string(template_partial, context, request=request)


def custom_question(request):
    res, q = validate_for_question(request, request.session.get('question_order', None), navigate=False)
    if not(res):
        return q
    html = get_question(request, q)
    print(f"{Colors.INFO}[INFO]: Question {q.pk} sent for user {request.session['username']}{Colors.RESET}")
    return JsonResponse({
        'success': True,
        'html': html,
    })

@timer
def next_question(request):
    res, q = validate_for_question(request, request.session.get('question_order', None) + 1)
    if not(res):
        return q
    html = get_question(request, q)
    print(f"{Colors.INFO}[INFO]: Question {q.pk} sent for user {request.session['username']}{Colors.RESET}")
    return JsonResponse({
        'success': True,
        'html': html,
    })

def pre_question(request):
    res, q = validate_for_question(request, request.session.get('question_order', None) - 1)
    if not(res):
        return q
    html = get_question(request, q)
    print(f"{Colors.INFO}[INFO]: Question {q.pk} sent for user {request.session['username']}{Colors.RESET}")
    return JsonResponse({
        'success': True,
        'html': html,
    })
    