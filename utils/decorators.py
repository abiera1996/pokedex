from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User

 

def require_not_logged(function):
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated: 
            return redirect(reverse('web:pokemon'))

        return function(request, *args, **kwargs) 

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


class require_logged(object):
 
    def __init__(self, roles=[], permission_code=None):
        self.roles = roles
        self.permission_code = permission_code
        
    def __call__(self, original_func):
        def wrap(request, *args, **kwargs): 
            if request.user.is_authenticated:    
                return original_func(request, *args, **kwargs)
            return redirect('web:logout') 
        return wrap