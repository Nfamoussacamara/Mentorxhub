from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from mentoring.forms import MenteeOnboardingForm, MentorOnboardingForm
from mentoring.models import StudentProfile, MentorProfile, MentoringSession
from accounts.forms import UserProfileImageForm


class ProfileDisplayView(LoginRequiredMixin, TemplateView):
    """Vue pour afficher le profil utilisateur avec toutes les données onboarding"""
    template_name = 'accounts/profile.html'
    login_url = 'accounts:login'
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifier que l'utilisateur a un rôle valide"""
        if request.user.role not in ['student', 'mentor']:
            messages.warning(request, "Veuillez d'abord sélectionner un rôle.")
            return redirect('accounts:onboarding_role')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Récupérer toutes les données du profil"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['is_student'] = user.role == 'student'
        context['is_mentor'] = user.role == 'mentor'
        
        # Récupérer le profil selon le rôle
        if user.role == 'student':
            profile, created = StudentProfile.objects.get_or_create(user=user)
            context['profile'] = profile
            
            # Récupérer les sessions de mentoring
            sessions = MentoringSession.objects.filter(student=profile).order_by('-date', '-start_time')[:5]
            context['recent_sessions'] = sessions
            context['total_sessions'] = profile.total_sessions
            
        elif user.role == 'mentor':
            profile, created = MentorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'status': 'pending',
                    'expertise': '',
                    'years_of_experience': 0,
                    'hourly_rate': 0.0,
                    'languages': ''
                }
            )
            context['profile'] = profile
            
            # Récupérer les sessions de mentoring
            sessions = MentoringSession.objects.filter(mentor=profile).order_by('-date', '-start_time')[:5]
            context['recent_sessions'] = sessions
            context['total_sessions'] = profile.total_sessions
            context['rating'] = profile.rating
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Vue pour modifier le profil utilisateur (réutilise les formulaires onboarding)"""
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    login_url = 'accounts:login'
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifier que l'utilisateur a un rôle valide"""
        if request.user.role not in ['student', 'mentor']:
            messages.warning(request, "Veuillez d'abord sélectionner un rôle.")
            return redirect('accounts:onboarding_role')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_class(self):
        """Retourner le formulaire approprié selon le rôle"""
        if self.request.user.role == 'student':
            return MenteeOnboardingForm
        elif self.request.user.role == 'mentor':
            return MentorOnboardingForm
        return None
    
    def get_object(self, queryset=None):
        """Retourner le profil approprié selon le rôle"""
        if self.request.user.role == 'student':
            profile, created = StudentProfile.objects.get_or_create(
                user=self.request.user
            )
            return profile
        elif self.request.user.role == 'mentor':
            profile, created = MentorProfile.objects.get_or_create(
                user=self.request.user,
                defaults={
                    'status': 'pending',
                    'expertise': '',
                    'years_of_experience': 0,
                    'hourly_rate': 0.0,
                    'languages': ''
                }
            )
            return profile
        return None
    
    def get_context_data(self, **kwargs):
        """Ajouter des informations supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_student'] = self.request.user.role == 'student'
        context['is_mentor'] = self.request.user.role == 'mentor'
        context['image_form'] = UserProfileImageForm(instance=self.request.user)
        return context
    
    def form_valid(self, form):
        """Gérer la soumission du formulaire"""
        messages.success(self.request, 'Votre profil a été mis à jour avec succès.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Gérer les erreurs du formulaire"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        """Gérer la soumission du formulaire avec les images"""
        # Si c'est pour sauvegarder les images uniquement
        if 'save_images' in request.POST:
            image_form = UserProfileImageForm(request.POST, request.FILES, instance=request.user)
            if image_form.is_valid():
                image_form.save()
                messages.success(request, 'Vos images ont été mises à jour avec succès.')
                return redirect('accounts:profile_edit')
            else:
                # Si le formulaire d'images est invalide, on affiche les erreurs
                for field, errors in image_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
                return redirect('accounts:profile_edit')
        
        # Sinon, traiter le formulaire principal
        return super().post(request, *args, **kwargs)

