from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Accounts  # Import your Accounts model or use the appropriate import path

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:

                if hasattr(request.user, 'role') and request.user.role == role:
                    return view_func(request, *args, **kwargs)
                else:
                    logout(request)  # Log out the user
                    # Redirect to the login page or any other desired location
                    return redirect('login')
            else:
                logout(request)
                return redirect('login')
        return _wrapped_view
    return decorator

admin_role_required = role_required(Accounts.ADMIN)
employee_role_required = role_required(Accounts.EMPLOYEE)
