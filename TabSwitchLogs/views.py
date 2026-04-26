from django.http import JsonResponse
from django.utils import timezone
from TabSwitchLogs.models import TabSwitchLog
import json
from django.views.decorators.http import require_POST
from main.constant import EventType
import time
from colorama import Fore, Style
from main.constant import Colors
from main.views import get_time_now

@require_POST
def blur_activity(request):
    session_id = request.session.get('exam_session_id')
    role = request.session.get('role') 
    username = request.session.get('username')
    user_pk = request.session.get('user_id')
    if (not user_pk):
        return JsonResponse({'status': 'error'})
    
    data = json.loads(request.body)
    
    # try:
    #     user = User.objects.select_related("student").get(pk=user_pk)
    # except ObjectDoesNotExist:
    #     return JsonResponse({'status': 'error'})
    # except Exception:
    #     return JsonResponse({'status': 'error'})
    
    if (role == "student"):
        event = data.get('event')
        now = time.time()
        last_time = request.session.get('last_time')
        seconds = (now - last_time) if (last_time) else 0
        # student = user.student
        if (event == 'window_blur'):
            event_type = EventType.WINDOW_BLUR
            print(f"{Colors.WARNING}[WARNING]: User {username} clicked outside of the exam page{Colors.RESET}")
            print(f'{Colors.INFO}[INFO]: User focus was on the exam page for {seconds:.2f} seconds{Colors.RESET}')
        elif (event == 'window_focus'):
            event_type = EventType.WINDOW_FOCUS
            print(f"{Colors.WARNING}[WARNING]: User {username} returned to the exam page{Colors.RESET}")
            print(f'{Colors.INFO}[INFO]: User focus was not on the exam page for {seconds:.2f} seconds{Colors.RESET}')
        elif (event == 'window_hidden'):
            event_type = EventType.WINDOW_HIDDEN
            print(f'{Colors.WARNING}[WARNING]: The exam page went out of view for the user {username}{Colors.RESET}')
            print(f'{Colors.INFO}[INFO]: The exam was visibile for user for {seconds:.2f} seconds{Colors.RESET}')
        else:
            event_type = EventType.WINDOW_VISIBLE
            print(f'{Colors.WARNING}[WARNING]: The exam page was displayed to the user {username} again{Colors.RESET}')
            print(f'{Colors.INFO}[INFO]: The exam page was hidden for user for {seconds:.2f} seconds{Colors.RESET}')
        
        request.session['last_time'] = now

        TabSwitchLog.objects.create(
            SessionKey_id=session_id,
            QuestionKey_id=None,
            EventTime=get_time_now(),
            EventType=event_type,
            Duration=seconds
        )

    return JsonResponse({"status": "ok"})
    

