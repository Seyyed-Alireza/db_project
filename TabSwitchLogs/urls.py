from django.urls import path
from . import views

app_name = 'TabSwitchLogs'

urlpatterns = [
    path('tab-switch/', views.blur_activity, name='blur_activity'),
]