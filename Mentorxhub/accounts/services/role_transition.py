from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from mentoring.models import MentorProfile

class RoleTransitionService:
    @staticmethod
    def request_mentorship(user: CustomUser) -> MentorProfile:
        """
        Permet à un étudiant de demander à devenir mentor.
        Crée un profil mentor 'pending' sans changer le rôle user.
        """
        if user.role == 'mentor':
            raise ValidationError("L'utilisateur est déjà un mentor.")

        # Vérifier si une demande est déjà en cours
        if hasattr(user, 'mentor_profile'):
            profile = user.mentor_profile
            if profile.status == 'pending':
                raise ValidationError("Une demande est déjà en cours de traitement.")
            if profile.status == 'approved':
                raise ValidationError("L'utilisateur a déjà un profil mentor approuvé.")
            # Si rejeté, on peut potentiellement permettre une nouvelle demande 
            # (ici on réinitialise à pending)
            profile.status = 'pending'
            profile.save()
            return profile

        # Créer le profil mentor en attente
        profile = MentorProfile.objects.create(
            user=user,
            status='pending',
            # Valeurs par défaut obligatoires pour la création, 
            # devront être remplies via le formulaire d'onboarding
            expertise='À définir',
            years_of_experience=0,
            hourly_rate=0.0,
            languages='À définir'
        )
        return profile

    @staticmethod
    def approve_mentorship(user: CustomUser, admin_user: CustomUser) -> CustomUser:
        """
        Valide la transition d'un utilisateur vers le rôle mentor.
        Change le rôle de l'utilisateur et approuve le profil.
        """
        if not admin_user.is_staff:
            raise ValidationError("Seul un administrateur peut valider cette demande.")

        if not hasattr(user, 'mentor_profile'):
             raise ValidationError("Aucun profil mentor associé à cet utilisateur.")

        profile = user.mentor_profile
        
        with transaction.atomic():
            # 1. Mettre à jour le profil
            profile.status = 'approved'
            profile.save()
            
            # 2. Mettre à jour le rôle utilisateur
            user.role = 'mentor'
            user.save()
            
            # TODO: Envoyer une notification email ici

        return user
