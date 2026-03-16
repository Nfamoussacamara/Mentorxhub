from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from mentoring.models import MentorProfile
from mentoring.forms import MentorOnboardingForm

class MentorOnboardingView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MentorProfile
    form_class = MentorOnboardingForm
    template_name = 'mentoring/onboarding/mentor_form.html'
    
    def test_func(self):
        """Vérifie que l'utilisateur est bien un mentor"""
        return self.request.user.role == 'mentor'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:dashboard')

    def get_object(self):
        # Récupère ou crée le profil mentor associé à l'utilisateur connecté
        # Cela évite le crash RelatedObjectDoesNotExist si le profil n'a pas été créé
        # lors de l'inscription/sélection du rôle.
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

    def form_valid(self, form):
        # Marquer comme "En attente" lors de la soumission
        form.instance.status = 'pending'
        
        # Important : Marquer l'onboarding utilisateur comme complété
        self.request.user.onboarding_completed = True
        self.request.user.save()
        
        # Force le rechargement de la session pour mettre à jour les perms
        # (Parfois nécessaire si le backend d'auth met en cache)
        
        messages.success(self.request, "Votre demande a été soumise et est en attente de validation.")
        return super().form_valid(form)
