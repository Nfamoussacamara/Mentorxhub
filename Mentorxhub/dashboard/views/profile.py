"""
Vues du module Profil pour le Dashboard
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from accounts.forms import UserProfileImageForm
from mentoring.models import MentorProfile, StudentProfile, MentoringSession, Subject
from mentoring.forms import MenteeOnboardingForm, MentorOnboardingForm


@login_required
def profile_view(request):
    """Vue du profil utilisateur dans le dashboard"""
    user = request.user
    
    # Récupérer le profil selon le rôle
    profile = None
    stats = {}
    recent_activity = []
    
    if user.role == 'student':
        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=user)
        
        # Statistiques étudiant
        sessions = MentoringSession.objects.filter(student=profile)
        stats = {
            'total_sessions': sessions.count(),
            'completed_sessions': sessions.filter(status='completed').count(),
            'upcoming_sessions': sessions.filter(status='scheduled', date__gte=timezone.now().date()).count(),
            'total_hours': sum(s.duration() / 60 for s in sessions.filter(status='completed')),
        }
        
        # Activité récente
        recent_activity = sessions.order_by('-date', '-start_time')[:10]
        
    elif user.role == 'mentor':
        try:
            profile = user.mentor_profile
        except MentorProfile.DoesNotExist:
            profile = MentorProfile.objects.create(user=user)
        
        # Statistiques mentor
        sessions = MentoringSession.objects.filter(mentor=profile)
        stats = {
            'total_sessions': sessions.count(),
            'completed_sessions': sessions.filter(status='completed').count(),
            'pending_requests': sessions.filter(status='scheduled', date__gte=timezone.now().date()).count(),
            'avg_rating': sessions.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg'] or 0.0,
            'total_earnings': sum(s.duration() / 60 * float(profile.hourly_rate) for s in sessions.filter(status='completed')),
        }
        
        # Activité récente
        recent_activity = sessions.order_by('-date', '-start_time')[:10]
    
    # Calculer le pourcentage de complétion du profil
    completion_percentage = calculate_profile_completion(user, profile)
    
    context = {
        'user': user,
        'profile': profile,
        'stats': stats,
        'recent_activity': recent_activity,
        'completion_percentage': completion_percentage,
        'user_role': user.role,
    }
    
    # Détecter si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/profile_view.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/profile/view.html', context)


@login_required
def profile_edit(request):
    """Vue d'édition du profil dans le dashboard"""
    user = request.user
    
    # Récupérer le profil
    profile = None
    form = None
    
    if user.role == 'student':
        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=user)
        form = MenteeOnboardingForm(instance=profile)
        
    elif user.role == 'mentor':
        try:
            profile = user.mentor_profile
        except MentorProfile.DoesNotExist:
            profile = MentorProfile.objects.create(user=user)
        form = MentorOnboardingForm(instance=profile)
    
    image_form = UserProfileImageForm(instance=user)
    
    context = {
        'user': user,
        'profile': profile,
        'form': form,
        'image_form': image_form,
        'user_role': user.role,
    }
    
    # Détecter si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/profile_edit.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/profile/edit.html', context)


@login_required
def profile_update(request):
    """Mise à jour du profil via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    user = request.user
    
    # Gérer l'upload d'images
    if 'save_images' in request.POST:
        image_form = UserProfileImageForm(request.POST, request.FILES, instance=user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'success': True, 'message': 'Images mises à jour avec succès'})
        else:
            return JsonResponse({'success': False, 'errors': image_form.errors}, status=400)
    
    # Gérer la mise à jour du profil
    if user.role == 'student':
        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=user)
        form = MenteeOnboardingForm(request.POST, instance=profile)
    elif user.role == 'mentor':
        try:
            profile = user.mentor_profile
        except MentorProfile.DoesNotExist:
            profile = MentorProfile.objects.create(user=user)
        form = MentorOnboardingForm(request.POST, instance=profile)
    else:
        return JsonResponse({'error': 'Invalid role'}, status=400)
    
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Profil mis à jour avec succès'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def calculate_profile_completion(user, profile):
    """Calcule le pourcentage de complétion du profil"""
    if not profile:
        return 0
    
    total_fields = 0
    filled_fields = 0
    
    # Champs utilisateur
    user_fields = ['first_name', 'last_name', 'bio']
    for field in user_fields:
        total_fields += 1
        if getattr(user, field, None):
            filled_fields += 1
    
    # Champs selon le rôle
    if user.role == 'mentor' and isinstance(profile, MentorProfile):
        mentor_fields = ['expertise', 'years_of_experience', 'hourly_rate', 'languages', 'bio']
        for field in mentor_fields:
            total_fields += 1
            value = getattr(profile, field, None)
            if value and (isinstance(value, str) and value.strip() or isinstance(value, (int, float)) and value > 0):
                filled_fields += 1
    elif user.role == 'student' and isinstance(profile, StudentProfile):
        student_fields = ['level', 'bio', 'github_profile']
        for field in student_fields:
            total_fields += 1
            value = getattr(profile, field, None)
            if value and (isinstance(value, str) and value.strip()):
                filled_fields += 1
    
    # Images
    total_fields += 2
    if user.profile_picture:
        filled_fields += 1
    if user.banner_image:
        filled_fields += 1
    
    if total_fields == 0:
        return 0
    
    return int((filled_fields / total_fields) * 100)


@login_required
def complete_profile(request):
    """Vue pour compléter le profil en plusieurs étapes"""
    user = request.user
    
    if request.method == 'POST':
        # Mettre à jour les informations utilisateur
        if 'first_name' in request.POST:
            user.first_name = request.POST.get('first_name', '')
        if 'last_name' in request.POST:
            user.last_name = request.POST.get('last_name', '')
        if 'bio' in request.POST:
            user.bio = request.POST.get('bio', '')
        
        # Gérer les fichiers uploadés
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        if 'banner_image' in request.FILES:
            user.banner_image = request.FILES['banner_image']
        
        user.save()
        
        # Mettre à jour le profil selon le rôle
        if user.role == 'mentor':
            try:
                profile = user.mentor_profile
            except MentorProfile.DoesNotExist:
                profile = MentorProfile.objects.create(user=user)
            
            if 'expertise' in request.POST:
                profile.expertise = request.POST.get('expertise', '')
            if 'years_of_experience' in request.POST:
                try:
                    profile.years_of_experience = int(request.POST.get('years_of_experience', 0))
                except ValueError:
                    pass
            if 'hourly_rate' in request.POST:
                try:
                    profile.hourly_rate = float(request.POST.get('hourly_rate', 0))
                except ValueError:
                    pass
            if 'languages' in request.POST:
                profile.languages = request.POST.get('languages', '')
            if 'certifications' in request.POST:
                profile.certifications = request.POST.get('certifications', '')
            if 'linkedin_profile' in request.POST:
                profile.linkedin_profile = request.POST.get('linkedin_profile', '')
            if 'github_profile' in request.POST:
                profile.github_profile = request.POST.get('github_profile', '')
            if 'website' in request.POST:
                profile.website = request.POST.get('website', '')
            
            profile.save()
            
        elif user.role == 'student':
            try:
                profile = user.student_profile
            except StudentProfile.DoesNotExist:
                profile = StudentProfile.objects.create(user=user)
            
            if 'level' in request.POST:
                profile.level = request.POST.get('level', '')
            if 'learning_goals' in request.POST:
                profile.learning_goals = request.POST.get('learning_goals', '')
            if 'preferred_languages' in request.POST:
                profile.preferred_languages = request.POST.get('preferred_languages', '')
            if 'github_profile' in request.POST:
                profile.github_profile = request.POST.get('github_profile', '')
            
            # Gérer les centres d'intérêt (ManyToMany)
            if 'interests' in request.POST:
                interest_ids = request.POST.getlist('interests')
                profile.interests.set(interest_ids)
            
            profile.save()
        
        # Marquer l'onboarding comme complété
        user.onboarding_completed = True
        user.save()
        
        messages.success(request, 'Profil complété avec succès ! 🎉')
        return redirect('dashboard:dashboard')
    
    # GET request - Afficher le formulaire
    subjects = Subject.objects.filter(is_active=True).order_by('name') if user.role == 'student' else []
    
    # S'assurer que les profils existent
    if user.role == 'mentor':
        try:
            user.mentor_profile
        except MentorProfile.DoesNotExist:
            MentorProfile.objects.create(user=user)
    elif user.role == 'student':
        try:
            user.student_profile
        except StudentProfile.DoesNotExist:
            StudentProfile.objects.create(user=user)
    
    context = {
        'user': user,
        'subjects': subjects,
    }
    
    return render(request, 'dashboard/complete_profile.html', context)

