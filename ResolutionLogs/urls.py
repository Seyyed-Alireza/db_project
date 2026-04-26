from django.urls import path
from . import views

app_name = 'ResolutionLogs'

urlpatterns = [
    path('change-size/', views.change_size, name='change_size')
]