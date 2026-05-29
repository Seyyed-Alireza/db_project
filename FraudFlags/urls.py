from django.urls import path
from . import views

app_name = 'FraudFlags'

urlpatterns = [
    
    path('behavior/<int:exam_id>/<str:student_number>/', views.student_behaviour_diagram, name='behavior_diagram'),
]