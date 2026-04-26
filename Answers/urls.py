from django.urls import path
from . import views

app_name = 'Answers'

urlpatterns = [
    path('save-answer-d/<int:question_id>/', views.save_answer_d, name='save_answer'),
]