from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser
from mentoring.models import StudentProfile, MentorProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal qui crée automatiquement un profil Student ou Mentor
    quand un nouvel utilisateur est créé.
    """
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(
                user=instance,
                level='débutant',
                learning_goals='À définir',
                preferred_languages='Français'
            )
        elif instance.role == 'mentor':
            MentorProfile.objects.create(
                user=instance,
                expertise='À définir',
                years_of_experience=0,
                hourly_rate=50.00,
                languages='Français'
            )

