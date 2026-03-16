import logging

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from accounts.models import CustomUser

logger = logging.getLogger(__name__)


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """Déterminer dynamiquement la redirection après l'inscription."""
        return reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        """Créer un utilisateur avec le rôle choisi et le connecter."""
        # Récupérer le rôle sélectionné depuis les données du formulaire
        role = self.request.POST.get('role', 'student')
        if role not in dict(CustomUser.ROLE_CHOICES):
            messages.error(self.request, "Rôle invalide. Veuillez réessayer.")
            return redirect('accounts:signup')
        
        # Créer l'utilisateur avec le rôle
        user = form.save(commit=False)
        user.role = role
        
        # Sauvegarder l'utilisateur (cela déclenchera les signaux)
        user.save()
        
        # Le signal dashboard/signals.py crée automatiquement le UserProfile avec le bon rôle
        # car on a défini user.role avant le save()
        # Mais on s'assure quand même que le UserProfile a le bon rôle
        if hasattr(user, "user_profile"):
            if user.user_profile.role != role:
                user.user_profile.role = role
                user.user_profile.save(update_fields=["role"])
        
        # Spécifier le backend d'authentification car plusieurs sont configurés
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect('dashboard:dashboard')

    def form_invalid(self, form):
        # Stocker les erreurs dans les messages et rediriger (PRG pattern)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect('accounts:signup')


from django.http import HttpResponse

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        # Redirige les utilisateurs déjà connectés vers leur dashboard
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Traiter la connexion de l'utilisateur."""
        remember_me = self.request.POST.get('remember_me')

        # Si "se souvenir" n'est pas coché, la session expire quand le navigateur est fermé
        if not remember_me:
            self.request.session.set_expiry(60 * 60 * 4)  # 4 heures
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30 jours

        # Connexion de l'utilisateur
        response = super().form_valid(form)
        
        # Gestion de la redirection pour HTMX
        if self.request.headers.get('HX-Request'):
            success_url = self.get_success_url()
            return HttpResponse(status=200, headers={'HX-Redirect': success_url})

        return response

    def form_invalid(self, form):
        logger.warning(f"Échec de connexion: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        return redirect('accounts:login')


class CustomLogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, f'Au revoir {request.user.get_full_name()} ! À bientôt !')
            logout(request)
        return redirect('core:home')
