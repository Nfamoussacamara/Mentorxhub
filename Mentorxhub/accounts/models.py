from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour CustomUser sans username"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Créer et retourner un utilisateur avec email et mot de passe"""
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Créer et retourner un superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser doit avoir is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser doit avoir is_superuser=True'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé utilisant uniquement l'email"""
    
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('student', 'Étudiant'),
    )
    
    # Champs principaux
    email = models.EmailField(_('adresse email'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=150, blank=True)
    last_name = models.CharField(_('nom'), max_length=150, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    
    # Champs additionnels
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='banners/', null=True, blank=True)
    
    # Champs de permissions (requis par PermissionsMixin)
    is_staff = models.BooleanField(
        _('statut staff'),
        default=False,
        help_text=_('Détermine si l\'utilisateur peut se connecter à l\'admin')
    )
    is_active = models.BooleanField(
        _('actif'),
        default=True,
        help_text=_('Détermine si l\'utilisateur est actif')
    )
    
    # État de l'onboarding
    onboarding_completed = models.BooleanField(
        _('onboarding complété'),
        default=False,
        help_text=_('Indique si l\'utilisateur a terminé le parcours d\'onboarding')
    )
    
    # Dates
    date_joined = models.DateTimeField(_('date d\'inscription'), default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configuration
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'  # Utiliser email pour la connexion
    REQUIRED_FIELDS = ['role']  # Champs requis en plus de email et password
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.email
    
    def get_short_name(self):
        """Retourne le prénom de l'utilisateur"""
        return self.first_name or self.email.split('@')[0]
    
    def get_avatar_url(self):
        """Retourne l'URL de l'avatar (image uploadée ou avatar par défaut)"""
        try:
            if self.profile_picture and hasattr(self.profile_picture, 'url'):
                return self.profile_picture.url
        except (ValueError, AttributeError):
            pass
        # Générer un avatar par défaut avec UI Avatars
        name = self.get_full_name() or self.email
        # Nettoyer le nom pour l'URL
        name_clean = name.replace(' ', '+').replace('@', '')
        return f"https://ui-avatars.com/api/?name={name_clean}&size=200&background=4C6FFF&color=fff&bold=true"
