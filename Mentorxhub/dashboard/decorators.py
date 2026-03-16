"""
Décorateurs pour le dashboard
"""
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(role):
    """
    Décorateur qui vérifie que l'utilisateur a le rôle requis
    
    Usage:
        @role_required('mentor')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if request.user.role != role:
                raise PermissionDenied("Vous n'avez pas les permissions nécessaires.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def mentor_required(view_func):
    """Décorateur pour les vues réservées aux mentors"""
    return role_required('mentor')(view_func)


def student_required(view_func):
    """Décorateur pour les vues réservées aux étudiants"""
    return role_required('student')(view_func)
