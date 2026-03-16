"""
Signals pour le dashboard MentorXHub
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, DashboardSettings, Activity

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un UserProfile et DashboardSettings lors de la création d'un utilisateur"""
    if created:
        # Créer UserProfile seulement s'il n'existe pas déjà
        # Récupérer le rôle de l'utilisateur
        user_role = getattr(instance, 'role', None)
        
        # S'assurer que le rôle est toujours une valeur valide pour UserProfile
        # UserProfile a des choix différents de CustomUser (inclut 'admin')
        # IMPORTANT: On doit TOUJOURS passer un rôle valide dans defaults,
        # car get_or_create avec defaults vide ne déclenche pas le default du modèle
        if user_role and user_role in ['mentor', 'student', 'admin']:
            # Le rôle de l'utilisateur est valide pour UserProfile
            profile_role = user_role
        else:
            # Le rôle n'est pas défini ou n'est pas valide, utiliser 'student' par défaut
            profile_role = 'student'
        
        # Créer le profil avec le rôle défini explicitement
        profile, created_profile = UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': profile_role}
        )
        
        # Créer DashboardSettings
        DashboardSettings.objects.get_or_create(user=instance)
        
        # Créer une activité de connexion seulement si le profil a été créé
        if created_profile:
            Activity.objects.create(
                user=instance,
                action_type='login',
                description=f"Compte créé pour {instance.get_full_name()}",
                metadata={'email': instance.email}
            )


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    """Met à jour le UserProfile si l'utilisateur est mis à jour"""
    if hasattr(instance, 'user_profile'):
        # Synchroniser le rôle si nécessaire
        if instance.role != instance.user_profile.role:
            instance.user_profile.role = instance.role
            instance.user_profile.save(update_fields=['role'])

