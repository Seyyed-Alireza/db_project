from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ajax-logout/', views.ajax_logout, name='ajax_logout'),
]