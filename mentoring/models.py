from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser, MentorProfile, StudentProfile
from django.utils import timezone


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
        ('scheduled', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    )

    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='mentoring_sessions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='mentoring_sessions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"Session: {self.title} - {self.mentor.user.get_full_name()} avec {self.student.user.get_full_name()}"

    def duration(self):
        """Calcule la durée de la session en minutes"""
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return (end - start).total_seconds() / 60

