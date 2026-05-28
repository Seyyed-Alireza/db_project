from functools import wraps
from django.shortcuts import redirect

def session_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('Users:login')  
        return view_func(request, *args, **kwargs)
    return _wrapped