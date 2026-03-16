from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MentoringSession
from dashboard.models import Notification

@receiver(post_save, sender=MentoringSession)
def notify_session_status_change(sender, instance, created, **kwargs):
    """
    Envoie des notifications lors des changements d'état des sessions.
    Gère à la fois les sessions classiques et les sessions ouvertes.
    """
    # NOUVEAUX : Notification lors de la création d'une session ouverte
    if created and instance.status == 'available':
        # Pas de notification pour les sessions ouvertes à la création
        # Les étudiants les découvrent via la liste
        return
    
    # Session classique : demande à un mentor spécifique
    if created and instance.status == 'pending':
        # Notification au mentor pour une nouvelle demande
        Notification.objects.create(
            user=instance.mentor.user,
            type='new_request',
            title='Nouvelle demande de session',
            message=f"{instance.student.user.get_full_name()} souhaite réserver une session : {instance.title}",
            link='/mentoring/sessions/' # Idéalement lien vers la session
        )
        return

    # Si c'est une mise à jour
    if not created:
        # NOUVEAU : Session ouverte réservée (available -> scheduled)
        if instance.status == 'scheduled' and kwargs.get('update_fields') is None:
            # Vérifier s'il y a un changement de student (réservation)
            try:
                old_instance = MentoringSession.objects.get(pk=instance.pk)
                if old_instance.student is None and instance.student is not None:
                    # Une session ouverte vient d'être réservée !
                    Notification.objects.create(
                        user=instance.mentor.user,
                        type='session_confirmed',
                        title='Session réservée !',
                        message=f"{instance.student.user.get_full_name()} a réservé votre session '{instance.title}'.",
                        link=f'/mentoring/sessions/{instance.id}/'
                    )
                    return
            except MentoringSession.DoesNotExist:
                pass
        
        # Session acceptée par le mentor (pending -> scheduled)
        if instance.status == 'scheduled':
            # Notification à l'étudiant que la session est acceptée
             Notification.objects.create(
                user=instance.student.user,
                type='session_confirmed',
                title='Session confirmée !',
                message=f"Votre session '{instance.title}' avec {instance.mentor.user.get_full_name()} est confirmée.",
                link=f'/dashboard/sessions/{instance.id}/'
            )
        
        elif instance.status == 'rejected':
             # Notification à l'étudiant que la session est refusée
             Notification.objects.create(
                user=instance.student.user,
                type='session_cancelled', # Ou un type 'rejected' si dispo
                title='Demande de session refusée',
                message=f"Votre demande pour la session '{instance.title}' a été refusée par le mentor.",
                link='/mentoring/sessions/'
            )
