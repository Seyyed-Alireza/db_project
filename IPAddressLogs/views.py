from django.shortcuts import render
from db_project.FraudFlags.services import register_event
from Exams.models import Exam
from Students.models import Student
# Create your views here.
# exam_id = request.session.get('exam_id')
# student = Student.objects.get(pk=user_pk)
# exam = Exam.objects.get(pk=exam_id)

    
# register_event(student, exam, "ip_change")
