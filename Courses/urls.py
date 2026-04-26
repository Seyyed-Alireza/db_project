from django.urls import path
from . import views

app_name = 'Courses'

urlpatterns = [
    path('course/<int:course_id>/', views.course_page, name='course_page'),
]