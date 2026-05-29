from django.shortcuts import render, get_object_or_404
from TabSwitchLogs.models import TabSwitchLog
from IPAddressLogs.models import IPAddressLog
from Students.models import Student
from Exams.models import Exam
from ResolutionLogs.models import ResolutionLog

def student_behaviour_diagram(request, exam_id, student_number):
    student = get_object_or_404(Student, StudentNumber=student_number)
    # exam = get_object_or_404(Exam, pk=exam_id)

    tab_events = TabSwitchLog.objects.filter(
        SessionKey__ExamKey_id=exam_id,
        SessionKey__StudentKey__StudentNumber=student_number
    ).select_related('SessionKey')
    ip_events = IPAddressLog.objects.filter(
        SessionKey__ExamKey_id=exam_id,
        SessionKey__StudentKey__StudentNumber=student_number
    ).select_related('SessionKey')
    resolution_events = ResolutionLog.objects.filter(
        SessionKey__ExamKey_id=exam_id,
        SessionKey__StudentKey__StudentNumber=student_number
    ).select_related('SessionKey')
    events = []
    for log in tab_events:
        events.append({
            'time': log.EventTime,
            'type': 'تغییر تب',
            'details': f'مدت زمان: {log.Duration} ثانیه'
        })
    for log in ip_events:
        events.append({
            'time': log.LogTime,
            'type': 'تغییر IP',
            'details': f'آی‌پی: {log.IPAddress}' 
        })
    for log in resolution_events:
        events.append({
            'time': log.ChangeTime, 
            'type': 'تغییر سایز پنجره',
            'details': f'سایز پنجره: {log.WindowWidth}x{log.WindowHeight}'
        })

    events.sort(key=lambda x: x['time'])

    return render(request, 'FraudFlags/behavior_diagram.html', {
        'events': events,
        'student': student,
        'exam': exam_id
    })
