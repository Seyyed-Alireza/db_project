from django.urls import path
from . import views

app_name = 'Exams'

urlpatterns = [
    path('exam/<int:course_id>/<int:exam_id>/', views.exam_page, name='exam_page'),
    path('exit-exam/', views.exit_exam, name='exit_exam'),
    path('delete-exam/<int:course_id>/', views.delete_exam, name='delete_exam'),
    path('create-exam/<int:course_id>', views.create_exam, name='create_exam'),
    path('edit-exam/<int:course_id>/<int:exam_id>', views.edit_exam, name='edit_exam'),
    path('question/<int:exam_id>/<int:course_id>/', views.question_page, name='question_page'),
]