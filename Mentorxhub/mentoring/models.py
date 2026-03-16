from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from django.utils import timezone

class Subject(models.Model):
    """Modèle pour les matières/sujets d'intérêt disponibles"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la matière")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Nom de l'icône (optionnel)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentor_profile')
    expertise = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    languages = models.CharField(max_length=200)
    certifications = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_sessions = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil Mentor de {self.user.get_full_name()}"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    level = models.CharField(max_length=50, blank=True, null=True)
    learning_goals = models.TextField(blank=True, null=True)
    interests = models.ManyToManyField(Subject, blank=True, related_name='students', verbose_name="Centres d'intérêt")
    # Garder l'ancien champ pour la migration progressive (sera supprimé plus tard)
    interests_old = models.CharField(max_length=200, blank=True, null=True, help_text="Ancien champ - à supprimer après migration")
    preferred_languages = models.CharField(max_length=200, blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    total_sessions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil Étudiant de {self.user.get_full_name()}"

class Availability(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=[
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Disponibilités"
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"Disponibilité de {self.mentor.user.get_full_name()} - {self.get_day_of_week_display()}"

class MentoringSession(models.Model):
    STATUS_CHOICES = (
        ('available', 'Disponible'),      # Nouvelle session ouverte à la réservation
        ('pending', 'En attente'),
        ('scheduled', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
        ('rejected', 'Refusée'),
    )

    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='mentoring_sessions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='mentoring_sessions', 
                                null=True, blank=True)  # Nullable pour sessions ouvertes
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        if self.student:
            return f"Session: {self.title} - {self.mentor.user.get_full_name()} avec {self.student.user.get_full_name()}"
        return f"Session: {self.title} - {self.mentor.user.get_full_name()} (Disponible)"
    
    def is_available(self):
        """Vérifie si la session est disponible à la réservation"""
        return self.status == 'available' and self.student is None

    def duration(self):
        """Calcule la durée de la session en minutes"""
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return (end - start).total_seconds() / 60
