from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from main.views import get_user
from ResolutionLogs.models import ResolutionLog
from LoginSessions.models import LoginSession
from main.constant import Colors
from main.views import get_time_now
import json
import time

@require_POST
def change_size(request):
    session_key = request.session.get('exam_session_id')
    if (not session_key):
        return JsonResponse({
            'status': 'error',
            'message': 'session_id_not_found'
        })
    
    username = request.session.get('username')
    
    data = json.loads(request.body)
    event = data.get('event')
    width = data.get('new_width')
    height = data.get('new_height')
    if (event == 'first_resolution'):
        print(f'{Colors.INFO}[INFO]: User {username} entered exam page with width {width} and height {height}{Colors.RESET}')
        start = time.time()
    elif (event == 'question'):
        print(f'{Colors.INFO}[INFO]: User {username} entered question page with width {width} and height {height}{Colors.RESET}')
    else:
        print(f'{Colors.INFO}[INFO]: User {username} changed exam page resolution{Colors.RESET}')
        print(f'{Colors.INFO}[INFO]: New width: {width} and new height: {height}{Colors.RESET}')

    ResolutionLog.objects.create(
        SessionKey_id=session_key,
        ScreenWidth=None,
        ScreenHeight=None,
        WindowWidth=width,
        WindowHeight=height,
        ChangeTime=get_time_now()
    )

    return JsonResponse({
        'status': 'success'
    })
    
