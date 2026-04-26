from django.urls import path
from . import views

app_name = 'Questions'

urlpatterns = [
    path('get-question/', views.get_question, name='get_question'),
]