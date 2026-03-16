"""
Modèles Django pour le Dashboard MentorXHub
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()

# Import des managers
from .managers import (
    NotificationManager, ConversationManager, CourseManager, 
    PaymentManager, SupportTicketManager
)


class UserProfile(models.Model):
    """
    Profil utilisateur étendu avec toutes les informations nécessaires
    """
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('student', 'Mentoré'),
        ('admin', 'Administrateur'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True, max_length=1000)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    
    # Réseaux sociaux
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    
    # Localisation
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Préférences
    language = models.CharField(max_length=10, default='fr')
    currency = models.CharField(max_length=3, default='EUR')
    
    # Statistiques
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_sessions = models.PositiveIntegerField(default=0)
    courses_completed = models.PositiveIntegerField(default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        indexes = [
            models.Index(fields=['user', 'role']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Profile de {self.user.get_full_name()}"
    
    def get_avatar_url(self):
        """Retourne l'URL de l'avatar ou un avatar par défaut"""
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.user.get_full_name()}&background=3b82f6&color=fff&size=200"
    
    def get_banner_url(self):
        """Retourne l'URL de la bannière ou une bannière par défaut"""
        if self.banner:
            return self.banner.url
        return None


class DashboardSettings(models.Model):
    """
    Paramètres du dashboard pour chaque utilisateur
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_settings'
    )
    
    # Thème
    theme = models.CharField(
        max_length=10,
        choices=[('light', 'Clair'), ('dark', 'Sombre'), ('auto', 'Automatique')],
        default='light'
    )
    sidebar_collapsed = models.BooleanField(default=False)
    
    # Langue
    language = models.CharField(max_length=10, default='fr')
    
    # Notifications
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    session_reminders = models.BooleanField(default=True)
    
    # Confidentialité
    profile_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    show_activity = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Dashboard Settings')
        verbose_name_plural = _('Dashboard Settings')
    
    def __str__(self):
        return f"Settings de {self.user.get_full_name()}"


class Activity(models.Model):
    """
    Journal d'activité utilisateur
    """
    ACTION_TYPES = (
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('profile_update', 'Mise à jour profil'),
        ('session_create', 'Création session'),
        ('session_join', 'Rejoindre session'),
        ('course_start', 'Début cours'),
        ('course_complete', 'Cours terminé'),
        ('message_sent', 'Message envoyé'),
        ('payment_made', 'Paiement effectué'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_type_display()}"


class Conversation(models.Model):
    """
    Conversation entre utilisateurs
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    subject = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    
    objects = ConversationManager()
    
    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
        ]
    
    def __str__(self):
        return f"Conversation {self.id}"
    
    def get_last_message(self):
        """Retourne le dernier message de la conversation"""
        return self.messages.order_by('-created_at').first()
    
    def get_unread_count(self, user):
        """Retourne le nombre de messages non lus pour un utilisateur"""
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    """
    Message dans une conversation
    """
    STATUS_CHOICES = (
        ('sent', 'Envoyé'),
        ('delivered', 'Livré'),
        ('read', 'Lu'),
        ('archived', 'Archivé'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Fichiers attachés
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    attachment_name = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"Message de {self.sender.get_full_name()}"
    
    def mark_as_read(self):
        """Marque le message comme lu"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.status = 'read'
            self.save(update_fields=['is_read', 'read_at', 'status'])


class Course(models.Model):
    """
    Cours de mentorat
    """
    DIFFICULTY_CHOICES = (
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_courses',
        limit_choices_to={'user_profile__role': 'mentor'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    
    # Métadonnées
    students_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_lessons = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CourseManager()
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mentor', '-created_at']),
            models.Index(fields=['is_published', '-created_at']),
        ]
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Leçon d'un cours
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()  # Contenu HTML/Markdown
    video_url = models.URLField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ['course', 'order']
        indexes = [
            models.Index(fields=['course', 'order']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class CourseProgress(models.Model):
    """
    Progression d'un étudiant dans un cours
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_progresses'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='progresses'
    )
    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name='completed_by')
    quiz_scores = models.JSONField(default=dict, blank=True)  # {lesson_id: score}
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Course Progress')
        verbose_name_plural = _('Course Progresses')
        unique_together = ['student', 'course']
        indexes = [
            models.Index(fields=['student', '-last_accessed']),
            models.Index(fields=['course', '-progress_percentage']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.title}"
    
    def update_progress(self):
        """Met à jour le pourcentage de progression"""
        total_lessons = self.course.lessons.count()
        if total_lessons > 0:
            completed = self.completed_lessons.count()
            self.progress_percentage = (completed / total_lessons) * 100
            if self.progress_percentage >= 100 and not self.completed_at:
                self.completed_at = timezone.now()
            self.save(update_fields=['progress_percentage', 'completed_at'])


# Note: MentoringSession est défini dans mentoring/models.py
# On l'importe pour les relations
from mentoring.models import MentoringSession as MentoringSessionModel


class Payment(models.Model):
    """
    Paiement et facturation
    """
    PAYMENT_TYPES = (
        ('session', 'Session de mentorat'),
        ('course', 'Cours'),
        ('subscription', 'Abonnement'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('processing', 'En traitement'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Relations - Utiliser les modèles existants de mentoring
    session = models.ForeignKey(
        MentoringSessionModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    
    # Transaction
    transaction_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    invoice_pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    # Métadonnées
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    objects = PaymentManager()
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"Paiement {self.id} - {self.amount} {self.currency}"
    
    def generate_invoice(self):
        """Génère une facture PDF (à implémenter)"""
        # TODO: Implémenter la génération de PDF
        pass


class SupportTicket(models.Model):
    """
    Ticket de support client
    """
    CATEGORY_CHOICES = (
        ('technical', 'Technique'),
        ('billing', 'Facturation'),
        ('account', 'Compte'),
        ('other', 'Autre'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    objects = SupportTicketManager()
    
    class Meta:
        verbose_name = _('Support Ticket')
        verbose_name_plural = _('Support Tickets')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', 'priority', '-created_at']),
        ]
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"


class TicketReply(models.Model):
    """
    Réponse à un ticket de support
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ticket_replies'
    )
    content = models.TextField()
    is_internal = models.BooleanField(default=False)  # Note interne pour le support
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Ticket Reply')
        verbose_name_plural = _('Ticket Replies')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Réponse à {self.ticket.subject}"


# Notification model
class Notification(models.Model):
    """
    Modèle pour les notifications in-app
    """
    TYPE_CHOICES = (
        ('session_reminder', 'Rappel de session'),
        ('session_confirmed', 'Session confirmée'),
        ('session_cancelled', 'Session annulée'),
        ('new_message', 'Nouveau message'),
        ('new_request', 'Nouvelle demande'),
        ('payment_received', 'Paiement reçu'),
        ('review_received', 'Avis reçu'),
        ('system', 'Système'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='system'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = NotificationManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
    
    def mark_as_read(self):
        """Marque la notification comme lue"""
        self.is_read = True
        self.save(update_fields=['is_read'])
