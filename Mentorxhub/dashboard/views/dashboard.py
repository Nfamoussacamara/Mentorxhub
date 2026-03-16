"""
Vues du dashboard MentorXHub
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from mentoring.models import MentorProfile, StudentProfile, MentoringSession
from mentoring.forms import MenteeOnboardingForm, MentorOnboardingForm
from dashboard.models import Notification, Message, Activity, Course, CourseProgress, Conversation
from django.db.models import Prefetch
import json


@login_required
def dashboard(request):
    """
    Dashboard principal qui redirige vers la vue appropriée selon le rôle.
    Si l'utilisateur n'a pas de rôle, redirige vers la sélection de rôle.
    """
    user = request.user
    
    # Vérifier le rôle et rediriger vers le dashboard approprié
    if user.role == 'mentor':
        return mentor_dashboard(request)
    elif user.role == 'student':
        return student_dashboard(request)
    else:
        # Si pas de rôle défini, rediriger vers la sélection de rôle
        return redirect('accounts:onboarding_role')


@login_required
def mentor_dashboard(request):
    """Dashboard pour les mentors"""
    from ..services import get_mentor_stats
    
    user = request.user
    
    # Vérifier si le profil mentor existe
    try:
        mentor_profile = user.mentor_profile
    except MentorProfile.DoesNotExist:
        # Si pas de profil mentor, créer un profil basique ou rediriger
        return render(request, 'dashboard/home.html', {
            'stats': {
                'sessions_created': 0,
                'sessions_open': 0,
                'active_earnings': 0.0,
                'active_students': 0,
            },
            'upcoming_sessions': [],
            'user_role': 'mentor',
            'chart_data': {},
            'leaderboard': [],
        })
    
    # Récupérer toutes les statistiques via le service
    context = get_mentor_stats(mentor_profile, user)
    
    # Onboarding form
    onboarding_form = None
    if not user.onboarding_completed:
        onboarding_form = MentorOnboardingForm(instance=mentor_profile)
    
    context['onboarding_form'] = onboarding_form
    
    # Détecter si c'est une requête HTMX ou AJAX
    if request.headers.get('HX-Request') == 'true' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourner uniquement le fragment pour éviter la duplication de la navbar
        return render(request, 'dashboard/fragments/overview_dashboard.html', context)
    
    return render(request, 'dashboard/home.html', context)


@login_required
def student_dashboard(request):
    """Dashboard pour les étudiants"""
    from ..services import get_student_stats
    
    user = request.user
    
    # Vérifier si le profil étudiant existe
    try:
        student_profile = user.student_profile
    except StudentProfile.DoesNotExist:
        # Si pas de profil étudiant, créer un profil basique ou rediriger
        return render(request, 'dashboard/home.html', {
            'stats': {
                'sessions_created': 0,
                'sessions_open': 0,
                'total_hours': 0,
                'active_mentors': 0,
            },
            'upcoming_sessions': [],
            'user_role': 'student',
            'chart_data': {},
            'leaderboard': [],
        })
    
    # Récupérer toutes les statistiques via le service
    context = get_student_stats(student_profile, user)
    
    # Le formulaire d'onboarding
    onboarding_form = None
    if not user.onboarding_completed:
        onboarding_form = MenteeOnboardingForm(instance=student_profile)
    
    context['onboarding_form'] = onboarding_form
    
    # Détecter si c'est une requête HTMX ou AJAX
    if request.headers.get('HX-Request') == 'true' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourner uniquement le fragment pour éviter la duplication de la navbar
        return render(request, 'dashboard/fragments/overview_dashboard.html', context)
    
    return render(request, 'dashboard/home.html', context)

