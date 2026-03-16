from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from mentoring.models import MentorProfile, StudentProfile, Availability, MentoringSession
from mentoring.forms import MentorProfileForm, StudentProfileForm, AvailabilityForm, MentoringSessionForm, MentorMentoringSessionForm, SessionFeedbackForm
from dashboard.utils import is_htmx_request

# Constantes pour les options de filtre
EXPERTISE_CHOICES = [
    ('', 'Toutes les expertises'),
    ('Web Development', 'Web Development'),
    ('Data Science', 'Data Science'),
    ('Mobile Development', 'Mobile Development'),
    ('DevOps', 'DevOps'),
    ('UI/UX Design', 'UI/UX Design'),
]

LANGUAGE_CHOICES = [
    ('', 'Toutes les langues'),
    ('Français', 'Français'),
    ('English', 'English'),
    ('Español', 'Español'),
]


# Vue pour lister tous les mentors disponibles
class MentorListView(ListView):
    """
    Vue qui affiche la liste de tous les mentors disponibles.
    Accessible à tous les utilisateurs (connectés ou non).
    """
    model = MentorProfile
    template_name = 'mentoring/mentor_list.html'
    context_object_name = 'mentors'
    paginate_by = 12  # 12 mentors par page

    def get_queryset(self):
        queryset = MentorProfile.objects.select_related('user').filter(
            user__is_active=True
        )
        
        # Filtrage par expertise
        expertise = self.request.GET.get('expertise')
        if expertise:
            queryset = queryset.filter(expertise__icontains=expertise)
        
        # Filtrage par langue
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(languages__icontains=language)
        
        # Recherche par nom
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(user__first_name__icontains=search) | queryset.filter(user__last_name__icontains=search)
        
        return queryset.order_by('-user__date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les valeurs actuelles des filtres
        expertise_filter = self.request.GET.get('expertise', '')
        language_filter = self.request.GET.get('language', '')
        search_query = self.request.GET.get('search', '')
        
        # Préparer les options de filtres avec état sélectionné
        context['expertise_options'] = [
            {
                'value': value,
                'label': label,
                'selected': value == expertise_filter
            }
            for value, label in EXPERTISE_CHOICES
        ]
        
        context['language_options'] = [
            {
                'value': value,
                'label': label,
                'selected': value == language_filter
            }
            for value, label in LANGUAGE_CHOICES
        ]
        
        # Informations sur les filtres actifs
        context['has_active_filters'] = bool(search_query or expertise_filter or language_filter)
        context['search_query'] = search_query
        
        # Statistiques
        context['total_mentors'] = MentorProfile.objects.count()
        
        # Permissions utilisateur pour affichage conditionnel
        context['can_book_sessions'] = (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'role') and 
            self.request.user.role == 'student'
        )
        
        return context
    
    def get_template_names(self):
        """Retourne le template approprié selon le type de requête"""
        if is_htmx_request(self.request):
            # Si la requête vise le contenu principal du dashboard, on envoie l'interface COMPLÈTE
            target = self.request.headers.get('HX-Target')
            if target == 'dashboard-content':
                return ['mentoring/fragments/mentor_full_list.html']
            # Pour les recherches/filtres internes, on n'envoie que la grille de résultats
            return ['mentoring/fragments/mentor_list_content.html']
        return ['mentoring/mentor_list.html']

class PublicMentorProfileView(DetailView):
    """
    Vue publique du profil mentor.
    Accessible à tous (ou seulement connectés).
    """
    model = MentorProfile
    template_name = 'mentoring/mentor_public_profile.html'
    context_object_name = 'mentor'

    def get_queryset(self):
        # Permet d'afficher tous les profils actifs
        return MentorProfile.objects.filter(user__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentor = self.object
        if mentor.languages:
            context['languages_list'] = [lang.strip() for lang in mentor.languages.split(',')]
        return context


class MentorProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue de mise à jour du profil mentor.
    Permet au mentor de modifier ses informations personnelles et professionnelles.
    Accessible uniquement aux utilisateurs avec le rôle 'mentor'.
    """
    model = MentorProfile
    form_class = MentorProfileForm
    template_name = 'mentoring/mentor_profile_update.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def test_func(self):
        return self.request.user.role == 'mentor'

    def form_valid(self, form):
        messages.success(self.request, 'Profil mis à jour avec succès.')
        return super().form_valid(form)

class StudentProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Vue détaillée du profil étudiant.
    Affiche les informations de l'étudiant et ses sessions de mentorat.
    Accessible uniquement aux utilisateurs avec le rôle 'student'.
    """
    model = StudentProfile
    template_name = 'mentoring/student_profile.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.role == 'student'

    def get_object(self):
        # Récupère ou crée le profil étudiant de l'utilisateur connecté
        student_profile, created = StudentProfile.objects.get_or_create(user=self.request.user)
        return student_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sessions à venir (incluant celles en attente)
        context['upcoming_sessions'] = self.object.mentoring_sessions.filter(
            status__in=['pending', 'scheduled', 'in_progress']
        ).order_by('date', 'start_time')
        
        # Historique des sessions
        context['past_sessions'] = self.object.mentoring_sessions.filter(
            status='completed'
        ).order_by('-date', '-start_time')
        
        # Nombre de mentors actifs (distincts)
        context['active_mentors'] = self.object.mentoring_sessions.filter(
            status__in=['pending', 'scheduled', 'completed']
        ).values('mentor').distinct().count()
        
        return context

class StudentProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue de mise à jour du profil étudiant.
    Permet à l'étudiant de modifier ses informations personnelles et ses objectifs.
    Accessible uniquement aux utilisateurs avec le rôle 'student'.
    """
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'mentoring/student_profile_update.html'
    success_url = reverse_lazy('mentoring:student_profile')

    def test_func(self):
        return self.request.user.role == 'student'

    def form_valid(self, form):
        messages.success(self.request, 'Profil mis à jour avec succès.')
        return super().form_valid(form)

class AvailabilityListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue listant les disponibilités d'un mentor.
    Affiche toutes les créneaux horaires disponibles pour les sessions.
    Accessible uniquement aux utilisateurs avec le rôle 'mentor'.
    """
    model = Availability
    template_name = 'mentoring/availability_list.html'
    context_object_name = 'availabilities'

    def test_func(self):
        return self.request.user.role == 'mentor'

    def get_queryset(self):
        return Availability.objects.filter(mentor=self.request.user.mentor_profile)

class AvailabilityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue de création d'une disponibilité.
    Permet au mentor d'ajouter un nouveau créneau horaire disponible.
    Accessible uniquement aux utilisateurs avec le rôle 'mentor'.
    """
    model = Availability
    form_class = AvailabilityForm
    template_name = 'mentoring/availability_form.html'
    success_url = reverse_lazy('mentoring:availability_list')

    def test_func(self):
        return self.request.user.role == 'mentor'

    def form_valid(self, form):
        form.instance.mentor = self.request.user.mentor_profile
        messages.success(self.request, 'Disponibilité ajoutée avec succès.')
        return super().form_valid(form)

class AvailabilityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue de mise à jour d'une disponibilité.
    Permet au mentor de modifier un créneau horaire existant.
    Accessible uniquement au mentor propriétaire de la disponibilité.
    """
    model = Availability
    form_class = AvailabilityForm
    template_name = 'mentoring/availability_form.html'
    success_url = reverse_lazy('mentoring:availability_list')

    def test_func(self):
        return self.get_object().mentor.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Disponibilité mise à jour avec succès.')
        return super().form_valid(form)

class AvailabilityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue de suppression d'une disponibilité.
    Permet au mentor de supprimer un créneau horaire.
    Accessible uniquement au mentor propriétaire de la disponibilité.
    """
    model = Availability
    template_name = 'mentoring/availability_confirm_delete.html'
    success_url = reverse_lazy('mentoring:availability_list')

    def test_func(self):
        return self.get_object().mentor.user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Disponibilité supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

class MentoringSessionListView(LoginRequiredMixin, ListView):
    """
    Vue listant les sessions de mentorat.
    Affiche les sessions selon le rôle de l'utilisateur (mentor ou étudiant).
    Accessible aux utilisateurs connectés.
    """
    model = MentoringSession
    template_name = 'mentoring/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        if self.request.user.role == 'mentor':
            return MentoringSession.objects.filter(mentor=self.request.user.mentor_profile)
        return MentoringSession.objects.filter(student=self.request.user.student_profile)

class MentoringSessionDetailView(LoginRequiredMixin, DetailView):
    """
    Vue détaillée d'une session de mentorat.
    Affiche les informations complètes d'une session.
    Pour les étudiants, affiche le formulaire de feedback si la session est terminée.
    Accessible aux participants de la session (mentor et étudiant).
    """
    model = MentoringSession
    template_name = 'mentoring/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'student' and self.object.status == 'completed':
            context['feedback_form'] = SessionFeedbackForm(instance=self.object)
        return context

class MentoringSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue de création d'une session de mentorat.
    Permet à l'étudiant de planifier une nouvelle session avec un mentor.
    Accessible uniquement aux utilisateurs avec le rôle 'student'.
    """
    model = MentoringSession
    form_class = MentoringSessionForm
    template_name = 'mentoring/session_form.html'
    success_url = reverse_lazy('mentoring:session_list')

    def test_func(self):
        return self.request.user.role == 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor'] = get_object_or_404(MentorProfile, id=self.kwargs.get('mentor_id'))
        return context

    def form_valid(self, form):
        form.instance.student = self.request.user.student_profile
        form.instance.mentor = get_object_or_404(MentorProfile, id=self.kwargs.get('mentor_id'))
        messages.success(self.request, 'Session créée avec succès.')
        return super().form_valid(form)

class MentorMentoringSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue de création d'une session par un mentor.
    Permet au mentor de planifier une session avec un étudiant.
    """
    model = MentoringSession
    form_class = MentorMentoringSessionForm
    template_name = 'mentoring/session_form.html'
    success_url = reverse_lazy('dashboard:sessions_calendar')

    def test_func(self):
        return self.request.user.role == 'mentor'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['mentor'] = self.request.user.mentor_profile
        return kwargs

    def form_valid(self, form):
        form.instance.mentor = self.request.user.mentor_profile
        messages.success(self.request, 'Session créée avec succès.')
        return super().form_valid(form)

class MentoringSessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue de mise à jour d'une session de mentorat.
    Permet de modifier les détails d'une session existante.
    Accessible aux participants de la session (mentor et étudiant).
    """
    model = MentoringSession
    form_class = MentoringSessionForm
    template_name = 'mentoring/session_form.html'
    success_url = reverse_lazy('mentoring:session_list')

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'mentor' and session.mentor.user == self.request.user) or \
               (self.request.user.role == 'student' and session.student.user == self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Session mise à jour avec succès.')
        return super().form_valid(form)

class MentoringSessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue de suppression d'une session de mentorat.
    Permet d'annuler une session planifiée.
    Accessible aux participants de la session (mentor et étudiant).
    """
    model = MentoringSession
    template_name = 'mentoring/session_confirm_delete.html'
    success_url = reverse_lazy('mentoring:session_list')

    def test_func(self):
        session = self.get_object()
        return (self.request.user.role == 'mentor' and session.mentor.user == self.request.user) or \
               (self.request.user.role == 'student' and session.student.user == self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Session supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

class SessionFeedbackView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue de feedback pour une session de mentorat.
    Permet à l'étudiant de laisser une évaluation et des commentaires sur une session terminée.
    Accessible uniquement à l'étudiant participant de la session.
    Met automatiquement à jour le statut de la session à 'completed'.
    """
    model = MentoringSession
    form_class = SessionFeedbackForm
    template_name = 'mentoring/session_feedback.html'
    success_url = reverse_lazy('mentoring:session_list')

    def test_func(self):
        session = self.get_object()
        return self.request.user.role == 'student' and session.student.user == self.request.user

    def form_valid(self, form):
        form.instance.status = 'completed'
        messages.success(self.request, 'Feedback envoyé avec succès.')
        return super().form_valid(form)


class SessionApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue pour approuver une session (Mentor uniquement)
    """
    def test_func(self):
        session = get_object_or_404(MentoringSession, pk=self.kwargs['pk'])
        return self.request.user.role == 'mentor' and session.mentor.user == self.request.user

    def post(self, request, pk):
        session = get_object_or_404(MentoringSession, pk=pk)
        if session.status == 'pending':
            session.status = 'scheduled'
            session.save()
            messages.success(request, 'Session confirmée avec succès.')
        return redirect('mentoring:session_list')


class SessionRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue pour refuser une session (Mentor uniquement)
    """
    def test_func(self):
        session = get_object_or_404(MentoringSession, pk=self.kwargs['pk'])
        return self.request.user.role == 'mentor' and session.mentor.user == self.request.user

    def post(self, request, pk):
        session = get_object_or_404(MentoringSession, pk=pk)
        if session.status == 'pending':
            session.status = 'rejected'
            session.save()
            messages.warning(request, 'Session refusée.')
        return redirect('mentoring:session_list')


# ===== NOUVELLES VUES POUR SESSIONS OUVERTES =====

class AvailableSessionListView(LoginRequiredMixin, ListView):
    """
    Vue listant les sessions disponibles à la réservation.
    Affiche toutes les sessions ouvertes (status='available', student=None).
    Accessible aux étudiants pour trouver et réserver des sessions.
    """
    model = MentoringSession
    template_name = 'mentoring/available_sessions_list.html'
    context_object_name = 'sessions'
    paginate_by = 12
    
    def get_queryset(self):
        from django.db.models import Q
        from datetime import date
        
        queryset = MentoringSession.objects.filter(
            status='available',
            student__isnull=True,
            date__gte=date.today()
        ).select_related('mentor__user').order_by('date', 'start_time')
        
        # Filtres optionnels
        expertise = self.request.GET.get('expertise')
        if expertise:
            queryset = queryset.filter(mentor__expertise__icontains=expertise)
        
        selected_date = self.request.GET.get('date')
        if selected_date:
            queryset = queryset.filter(date=selected_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Liste des expertises disponibles pour le filtre
        context['expertises'] = MentorProfile.objects.values_list('expertise', flat=True).distinct()
        context['selected_date'] = self.request.GET.get('date', '')
        return context


class MentorCreateAvailableSessionView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue pour créer une session ouverte (sans étudiant assigné).
    Accessible uniquement aux mentors.
    La session créée a le status 'available' et peut être réservée par n'importe quel étudiant.
    """
    model = MentoringSession
    template_name = 'mentoring/available_session_form.html'
    success_url = reverse_lazy('mentoring:session_list')
    
    def test_func(self):
        return self.request.user.role == 'mentor'
    
    def get_form_class(self):
        # Importer ici pour éviter les imports circulaires
        from mentoring.forms_available import AvailableSessionForm
        return AvailableSessionForm
    
    def form_valid(self, form):
        # Assigner le mentor connecté
        form.instance.mentor = self.request.user.mentor_profile
        # Pas d'étudiant assigné
        form.instance.student = None
        # Status: available
        form.instance.status = 'available'
        
        messages.success(self.request, 
                        'Session ouverte créée avec succès ! Les étudiants peuvent maintenant la réserver.')
        return super().form_valid(form)


class BookSessionView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vue pour réserver une session disponible.
    Accessible uniquement aux étudiants.
    Change le status de 'available' à 'scheduled' et assigne l'étudiant.
    """
    def test_func(self):
        # Vérifier que l'utilisateur est un étudiant ET a un profil étudiant
        return (self.request.user.role == 'student' and 
                hasattr(self.request.user, 'student_profile'))
    
    def handle_no_permission(self):
        messages.error(self.request, "Vous devez être un étudiant pour réserver une session.")
        return redirect('mentoring:available_sessions')
    
    def post(self, request, pk):
        session = get_object_or_404(MentoringSession, pk=pk)
        
        # Vérifier que la session existe et est disponible
        if session.status != 'available':
            messages.error(request, "Cette session n'est plus disponible.")
            return redirect('mentoring:available_sessions')
        
        # Vérifier que la session est toujours disponible
        if session.student is not None:
            messages.error(request, "Cette session a déjà été réservée par un autre étudiant.")
            return redirect('mentoring:available_sessions')
        
        # Vérifier que l'utilisateur a un profil étudiant
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, "Vous devez compléter votre profil étudiant pour réserver une session.")
            return redirect('mentoring:mentee_onboarding')
        
        # Assigner l'étudiant
        session.student = request.user.student_profile
        # Changer le status
        session.status = 'scheduled'
        session.save()
        
        messages.success(request, 
                       f"Session '{session.title}' réservée avec succès ! Rendez-vous le {session.date.strftime('%d/%m/%Y')} à {session.start_time.strftime('%H:%M')}.")
        
        return redirect('mentoring:session_detail', pk=pk)