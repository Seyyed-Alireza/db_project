from django.urls import path
from . import views

app_name = 'EduStaffs'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/create/', views.course_create, name='course_create'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('course/<int:course_id>/enrollments/', views.manage_enrollments, name='manage_enrollments'),
    path('course/<int:course_id>/remove/<int:student_id>/', views.remove_student_from_course, name='remove_student_from_course'),
    path('course/<int:course_id>/assign-teacher/', views.assign_teacher_to_course, name='assign_teacher_to_course'),


]