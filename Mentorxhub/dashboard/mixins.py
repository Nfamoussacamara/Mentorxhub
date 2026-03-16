"""
Mixins pour les permissions et fonctionnalités du dashboard
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class RoleRequiredMixin:
    """
    Mixin qui vérifie que l'utilisateur a le rôle requis
    """
    required_role = None  # 'mentor' ou 'student'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if self.required_role and request.user.role != self.required_role:
            raise PermissionDenied("Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        
        return super().dispatch(request, *args, **kwargs)


class MentorRequiredMixin(RoleRequiredMixin):
    """Mixin pour les vues réservées aux mentors"""
    required_role = 'mentor'


class StudentRequiredMixin(RoleRequiredMixin):
    """Mixin pour les vues réservées aux étudiants"""
    required_role = 'student'


class DashboardMixin(LoginRequiredMixin):
    """
    Mixin de base pour toutes les vues du dashboard
    Ajoute des fonctionnalités communes
    """
    login_url = '/accounts/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        return context
