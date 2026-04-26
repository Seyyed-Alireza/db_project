from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from .forms import LoginForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user = form.cleaned_data['user']

            User.objects.filter(pk=user.pk).update(IsLoggedIn=True)
            
            request.session['user_id']   = user.pk
            request.session['username']  = user.Username
            request.session['role']      = user.Role

            # messages.success(request, f'خوش آمدید، {user.FirstName}!')
            return redirect('main:mainpage')
        else:
            pass
            # messages.error(request, 'ورود ناموفق. لطفاً اطلاعات را بررسی کنید.')
    else:
        form = LoginForm()
    return render(request, 'Users/login.html', {'form': form})

def logout_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        User.objects.filter(pk=user_id).update(IsLoggedIn=False)
    request.session.flush()
    # messages.info(request, 'از سیستم خارج شدید.')
    return redirect('main:mainpage')

# views.py (اپ Users)

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def ajax_logout(request):
    user_id = request.session.get('user_id')
    # print("I was here")
    
    if user_id:
        from Users.models import User
        User.objects.filter(pk=user_id).update(IsLoggedIn=False)
        request.session.flush()
        
        return JsonResponse({'status': 'ok', 'message': 'Logged out successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'No user session found'})