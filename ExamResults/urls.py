from django.urls import path
from . import views

app_name = 'ExamResults'

urlpatterns = [
    path('exam-result/<int:exam_id>/', views.exam_result, name='exam_result'),
    path("exam/<int:exam_id>/grade/", views.grade_exam_students, name="grade_exam_students"),
    path("my-results/", views.student_results, name="student_results"),
]   