from django.urls import path
from . import views

app_name = 'Questions'

urlpatterns = [
    path('get-question/', views.custom_question, name='custom_question'),
    path('next-question/', views.next_question, name='next_question'),
    path('pre-question/', views.pre_question, name='pre_question'),
]