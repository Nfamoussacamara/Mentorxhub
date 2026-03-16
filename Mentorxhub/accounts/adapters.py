"""
Adapters personnalisés pour django-allauth.

Ce module configure le comportement de l'authentification sociale (Google OAuth)
et de l'inscription classique (email/password).
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    """
    Adapter pour l'inscription classique via email/password.
    
    Gère la logique métier spécifique lors de la création d'un compte
    avec formulaire (rôle, profil, etc.).
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Sauvegarde l'utilisateur avec les données du formulaire d'inscription.
        
        Args:
            request: La requête HTTP
            user: L'instance utilisateur à sauvegarder
            form: Le formulaire d'inscription contenant les données
            commit: Si True, sauvegarde en base de données
            
        Returns:
            L'instance utilisateur sauvegardée
        """
        user = super().save_user(request, user, form, commit=False)
        
        # La logique métier (rôle, etc.) sera gérée par le formulaire ou la vue
        # Nous ne définissons rien ici pour rester minimal
        
        if commit:
            user.save()
        
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adapter pour l'authentification Google OAuth.
    
    Objectifs:
    - Supprimer toute page intermédiaire django-allauth
    - Créer automatiquement un compte utilisateur minimal
    - Lier automatiquement les comptes existants
    - Ne pas gérer de logique métier (rôle, profil, etc.)
    """
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Détermine si la création automatique de compte est autorisée.
        
        Important:
        - Retourner True supprime la page "/accounts/3rdparty/signup/"
        - L'utilisateur est créé immédiatement après l'authentification Google
        
        Args:
            request: La requête HTTP
            sociallogin: Les informations de connexion sociale
            
        Returns:
            bool: True pour créer le compte automatiquement
        """
        return True
    
    def populate_user(self, request, sociallogin, data):
        """
        Remplit les informations de l'utilisateur à partir des données Google.
        
        Crée un utilisateur MINIMAL avec uniquement:
        - email (fourni par Google)
        - first_name (optionnel, fourni par Google)
        - last_name (optionnel, fourni par Google)
        
        AUCUNE logique métier ici (pas de rôle, pas de profil).
        
        Args:
            request: La requête HTTP
            sociallogin: Les informations de connexion sociale
            data: Les données fournies par Google
            
        Returns:
            L'instance utilisateur avec les données minimales
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Assigner le rôle par défaut 'student' si non défini
        if not hasattr(user, 'role') or not user.role:
            user.role = 'student'
            
        return user
    
    def pre_social_login(self, request, sociallogin):
        """
        Appelé avant la connexion sociale, permet de lier des comptes existants.
        
        Si un utilisateur existe déjà avec le même email:
        - On lie automatiquement le compte Google à cet utilisateur
        - Évite la création de doublons
        
        Args:
            request: La requête HTTP
            sociallogin: Les informations de connexion sociale
        """
        # Si l'utilisateur est déjà authentifié, ne rien faire
        if sociallogin.is_existing:
            return
        
        # Récupérer l'email depuis les données Google
        email = sociallogin.account.extra_data.get('email')
        
        # Si pas d'email, on ne peut pas faire de liaison
        if not email:
            return
        
        # Chercher un utilisateur existant avec cet email
        try:
            existing_user = User.objects.get(email=email)
            
            # Lier le compte Google à l'utilisateur existant
            # Cela évite la création d'un doublon
            sociallogin.connect(request, existing_user)
            
        except User.DoesNotExist:
            # Aucun utilisateur existant, django-allauth créera un nouveau compte
            pass
