from django.urls import path
from . import views

app_name = 'ExamResults'

urlpatterns = [
    path('exam-result/<int:exam_id>/', views.exam_result, name='exam_result'),
]