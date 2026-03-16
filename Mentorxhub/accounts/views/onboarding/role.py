from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from ...forms import RoleSelectionForm

class RoleSelectionView(LoginRequiredMixin, FormView):
    template_name = 'accounts/onboarding/role_selection.html'
    form_class = RoleSelectionForm
    
    def get_success_url(self):
        return reverse('dashboard:dashboard') # Ou onboarding/profile/ si implémenté

    def get(self, request, *args, **kwargs):
        # Si l'utilisateur a déjà un rôle, rediriger vers le dashboard
        if request.user.role:
            return redirect('dashboard:dashboard')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        role = form.cleaned_data['role']
        
        user.role = role
        user.save()
        
        if role == 'mentor':
            from mentoring.models import MentorProfile
            MentorProfile.objects.get_or_create(user=user)
        elif role == 'student':
            from mentoring.models import StudentProfile
            StudentProfile.objects.get_or_create(user=user)
        
        # Redirection vers l'étape suivante (Dashboard pour l'instant, ou Profil)
        messages.success(self.request, f"Rôle {role} sélectionné avec succès !")
        return super().form_valid(form)
