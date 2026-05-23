from django.urls import path
from . import views

app_name = 'Answers'

urlpatterns = [
    path('save-answer-d/<int:question_id>/', views.save_answer_d, name='save_answer_d'),
    path('save-answer-m/<int:question_id>/', views.save_answer_m, name='save_answer_m'),
    path('delete-selected-option/', views.delete_selected_option, name='delete_selected_option'),
]