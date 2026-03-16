"""
Utilitaires pour le dashboard
"""
from .models import Notification
from mentoring.models import MentoringSession
from django.utils import timezone
from datetime import timedelta


class NotificationService:
    """
    Service pour créer et gérer les notifications
    """
    
    @staticmethod
    def create_notification(user, type, title, message, link=None):
        """Crée une notification"""
        return Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
            link=link
        )
    
    @staticmethod
    def send_session_reminder(session):
        """Envoie un rappel de session 24h avant"""
        if session.status != 'scheduled':
            return
        
        session_datetime = timezone.make_aware(
            timezone.datetime.combine(session.date, session.start_time)
        )
        reminder_time = session_datetime - timedelta(hours=24)
        
        # Vérifier si on est dans la fenêtre de rappel (24h avant)
        now = timezone.now()
        if now >= reminder_time and now < session_datetime:
            # Notification pour l'étudiant
            NotificationService.create_notification(
                user=session.student.user,
                type='session_reminder',
                title='Rappel de session',
                message=f'Votre session "{session.title}" avec {session.mentor.user.get_full_name()} est demain à {session.start_time.strftime("%H:%M")}',
                link=f'/dashboard/sessions/{session.id}/'
            )
            
            # Notification pour le mentor
            NotificationService.create_notification(
                user=session.mentor.user,
                type='session_reminder',
                title='Rappel de session',
                message=f'Votre session "{session.title}" avec {session.student.user.get_full_name()} est demain à {session.start_time.strftime("%H:%M")}',
                link=f'/dashboard/sessions/{session.id}/'
            )
    
    @staticmethod
    def send_session_confirmed(session):
        """Notification de confirmation de session"""
        NotificationService.create_notification(
            user=session.student.user,
            type='session_confirmed',
            title='Session confirmée',
            message=f'Votre session "{session.title}" avec {session.mentor.user.get_full_name()} a été confirmée.',
            link=f'/dashboard/sessions/{session.id}/'
        )
        
        NotificationService.create_notification(
            user=session.mentor.user,
            type='session_confirmed',
            title='Session confirmée',
            message=f'La session "{session.title}" avec {session.student.user.get_full_name()} a été confirmée.',
            link=f'/dashboard/sessions/{session.id}/'
        )
    
    @staticmethod
    def send_new_request(session):
        """Notification de nouvelle demande de session"""
        NotificationService.create_notification(
            user=session.mentor.user,
            type='new_request',
            title='Nouvelle demande de session',
            message=f'{session.student.user.get_full_name()} a demandé une session "{session.title}"',
            link=f'/dashboard/sessions/{session.id}/'
        )


def is_htmx_request(request):
    """
    Vérifie si la requête est une requête HTMX ou AJAX.
    HTMX envoie le header HX-Request: true
    """
    return (
        request.headers.get('HX-Request') == 'true' or 
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    )


def render_for_htmx(request, full_template, fragment_template, context):
    """
    Rend le template approprié selon le type de requête.
    - Requête HTMX/AJAX : retourne uniquement le fragment
    - Requête normale : retourne la page complète avec base.html
    
    Args:
        request: La requête HTTP
        full_template: Template complet (extends base.html)
        fragment_template: Template fragment (contenu uniquement)
        context: Contexte du template
    
    Returns:
        HttpResponse avec le template approprié
    """
    from django.shortcuts import render
    
    if is_htmx_request(request):
        return render(request, fragment_template, context)
    return render(request, full_template, context)

