from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View

from mentoring.forms import MenteeOnboardingForm
from mentoring.models import StudentProfile


class MenteeOnboardingView(LoginRequiredMixin, CreateView):
    template_name = 'mentoring/onboarding/mentee_form.html'
    form_class = MenteeOnboardingForm
    success_url = reverse_lazy('dashboard:student')

    def get_form_kwargs(self):
        """Injecter l'utilisateur courant dans le formulaire."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = getattr(self.request.user, 'student_profile', None)
        return kwargs

    def form_valid(self, form):
        """Sauvegarder le profil et marquer l'onboarding comme complété."""
        # Sauvegarder le profil avec l'instance liée à l'utilisateur
        profile = form.save(commit=False)
        # S'assurer que le profil est bien lié à l'utilisateur actuel
        profile.user = self.request.user
        profile.save()  # Sauvegarder dans la base de données
        
        # Marquer l'onboarding comme complété
        user = self.request.user
        user.onboarding_completed = True
        user.save()
        
        return super().form_valid(form)


class SkipMenteeOnboardingView(LoginRequiredMixin, View):
    """Vue pour passer l'étape d'onboarding.
    
    Marque simplement l'onboarding comme complété sans sauvegarder de données.
    """
    
    def post(self, request, *args, **kwargs):
        """Passer l'onboarding et rediriger vers le dashboard."""
        user = request.user
        
        # Vérifier que c'est un mentoré
        if user.role != 'student':
            messages.warning(request, "Action non autorisée.")
            return redirect('dashboard:dashboard')
        
        # Créer un profil vide si nécessaire
        StudentProfile.objects.get_or_create(user=user)
        
        # Marquer l'onboarding comme complété
        user.onboarding_completed = True
        user.save()
        
        return redirect('dashboard:student')
