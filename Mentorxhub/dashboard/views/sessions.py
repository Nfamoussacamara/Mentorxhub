"""
Vues pour les sessions améliorées avec calendrier
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
from mentoring.models import MentoringSession, MentorProfile, StudentProfile, Availability
import hashlib


@login_required
def sessions_calendar(request):
    """Vue du calendrier des sessions"""
    user = request.user
    
    context = {
        'user_role': user.role,
    }
    
    # Détecter si c'est une requête AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/sessions_calendar.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/sessions/calendar.html', context)


@login_required
def sessions_events(request):
    """API endpoint pour les événements du calendrier"""
    user = request.user
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = []
    
    if user.role == 'mentor':
        try:
            mentor_profile = user.mentor_profile
            sessions = MentoringSession.objects.filter(
                mentor=mentor_profile
            )
            
            if start and end:
                start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
                sessions = sessions.filter(
                    date__gte=start_date.date(),
                    date__lte=end_date.date()
                )
            
            for session in sessions:
                session_datetime = timezone.make_aware(
                    datetime.combine(session.date, session.start_time)
                )
                end_datetime = timezone.make_aware(
                    datetime.combine(session.date, session.end_time)
                )
                
                color = {
                    'scheduled': '#3b82f6',
                    'in_progress': '#f59e0b',
                    'completed': '#10b981',
                    'cancelled': '#ef4444'
                }.get(session.status, '#6b7280')
                
                events.append({
                    'id': session.id,
                    'title': session.title,
                    'start': session_datetime.isoformat(),
                    'end': end_datetime.isoformat(),
                    'color': color,
                    'extendedProps': {
                        'status': session.status,
                        'student': session.student.user.get_full_name(),
                        'description': session.description,
                    }
                })
        except MentorProfile.DoesNotExist:
            pass
    
    elif user.role == 'student':
        try:
            student_profile = user.student_profile
            sessions = MentoringSession.objects.filter(
                student=student_profile
            )
            
            if start and end:
                start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
                sessions = sessions.filter(
                    date__gte=start_date.date(),
                    date__lte=end_date.date()
                )
            
            for session in sessions:
                session_datetime = timezone.make_aware(
                    datetime.combine(session.date, session.start_time)
                )
                end_datetime = timezone.make_aware(
                    datetime.combine(session.date, session.end_time)
                )
                
                color = {
                    'scheduled': '#3b82f6',
                    'in_progress': '#f59e0b',
                    'completed': '#10b981',
                    'cancelled': '#ef4444'
                }.get(session.status, '#6b7280')
                
                events.append({
                    'id': session.id,
                    'title': session.title,
                    'start': session_datetime.isoformat(),
                    'end': end_datetime.isoformat(),
                    'color': color,
                    'extendedProps': {
                        'status': session.status,
                        'mentor': session.mentor.user.get_full_name(),
                        'description': session.description,
                    }
                })
        except StudentProfile.DoesNotExist:
            pass
    
    return JsonResponse(events, safe=False)


@login_required
@require_http_methods(["POST"])
def session_update_date(request, session_id):
    """Mettre à jour la date d'une session (drag & drop)"""
    session = get_object_or_404(MentoringSession, id=session_id)
    
    # Vérifier les permissions
    user = request.user
    if user.role == 'mentor' and session.mentor.user != user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    elif user.role == 'student' and session.student.user != user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    new_date = request.POST.get('date')
    new_start_time = request.POST.get('start_time')
    new_end_time = request.POST.get('end_time')
    
    if new_date:
        session.date = datetime.fromisoformat(new_date).date()
    if new_start_time:
        session.start_time = datetime.fromisoformat(new_start_time).time()
    if new_end_time:
        session.end_time = datetime.fromisoformat(new_end_time).time()
    
    session.save()
    
    return JsonResponse({'success': True})


@login_required
def session_detail(request, session_id):
    """Détails d'une session"""
    session = get_object_or_404(MentoringSession, id=session_id)
    
    # Vérifier les permissions
    user = request.user
    if user.role == 'mentor' and session.mentor.user != user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    elif user.role == 'student' and session.student.user != user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    context = {
        'session': session,
        'user_role': user.role,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('dashboard/fragments/session_detail.html', context, request=request)
        return JsonResponse({'html': html}, safe=False)
    
    return render(request, 'dashboard/sessions/detail.html', context)


@login_required
def session_video_room(request, session_id):
    """Salle de visioconférence Jitsi pour une session"""
    session = get_object_or_404(MentoringSession, id=session_id)
    
    # Vérifier les permissions
    user = request.user
    if user.role == 'mentor' and session.mentor.user != user:
        return render(request, 'errors/403.html', status=403)
    elif user.role == 'student' and session.student.user != user:
        return render(request, 'errors/403.html', status=403)
    
    # Générer un nom de salle unique et sécurisé
    # On combine l'ID de la session avec un secret (facultatif mais recommandé)
    # On utilise un nom simple et prévisible pour Jitsi
    room_name = f"MentorXHub-Session-{session.id}"
    
    context = {
        'session': session,
        'room_name': room_name,
        'user_name': user.get_full_name() or user.email,
        'is_mentor': user.role == 'mentor',
        'hide_navbar': True,
        'hide_footer': True,
    }
    
    return render(request, 'dashboard/sessions/video_room.html', context)

