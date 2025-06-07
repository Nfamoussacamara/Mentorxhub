from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True  # Si l'utilisateur est déjà authentifié, il sera redirigé automatiquement (utile pour LoginView et CreateView)

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Bienvenue {user.get_full_name()} !')
            return redirect('home')
        else:
            messages.error(self.request, 'Email ou mot de passe incorrect.')
            return self.form_invalid(form)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True  # Si l'utilisateur est déjà authentifié, il sera redirigé automatiquement (utile pour LoginView et CreateView)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Bienvenue {user.get_full_name()} ! Votre compte a été créé avec succès.')
        return redirect('mentoring:student_update', pk=user.student_profile.pk) # Redirige vers la page de création du profil après l'inscription

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)

class CustomLogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, f'Au revoir {request.user.get_full_name()} ! À bientôt !')
            logout(request)
        return redirect('home')

