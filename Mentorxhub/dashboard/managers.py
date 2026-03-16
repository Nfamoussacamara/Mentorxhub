"""
Managers personnalisés pour les modèles du dashboard
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta


class NotificationManager(models.Manager):
    """Manager pour les notifications"""
    
    def unread(self, user):
        """Retourne les notifications non lues d'un utilisateur"""
        return self.filter(user=user, is_read=False)
    
    def recent(self, user, days=7):
        """Retourne les notifications récentes"""
        since = timezone.now() - timedelta(days=days)
        return self.filter(user=user, created_at__gte=since)


class ConversationManager(models.Manager):
    """Manager pour les conversations"""
    
    def for_user(self, user):
        """Retourne les conversations d'un utilisateur"""
        return self.filter(participants=user).distinct()
    
    def unread(self, user):
        """Retourne les conversations avec messages non lus"""
        conversations = self.for_user(user)
        return [conv for conv in conversations if conv.get_unread_count(user) > 0]


class CourseManager(models.Manager):
    """Manager pour les cours"""
    
    def published(self):
        """Retourne les cours publiés"""
        return self.filter(is_published=True)
    
    def for_mentor(self, mentor):
        """Retourne les cours d'un mentor"""
        return self.filter(mentor=mentor)
    
    def popular(self, limit=10):
        """Retourne les cours les plus populaires"""
        return self.published().order_by('-students_count', '-average_rating')[:limit]


class PaymentManager(models.Manager):
    """Manager pour les paiements"""
    
    def for_user(self, user):
        """Retourne les paiements d'un utilisateur"""
        return self.filter(user=user)
    
    def completed(self):
        """Retourne les paiements complétés"""
        return self.filter(status='completed')
    
    def pending(self):
        """Retourne les paiements en attente"""
        return self.filter(status='pending')


class SupportTicketManager(models.Manager):
    """Manager pour les tickets de support"""
    
    def for_user(self, user):
        """Retourne les tickets d'un utilisateur"""
        return self.filter(user=user)
    
    def open(self):
        """Retourne les tickets ouverts"""
        return self.filter(status__in=['open', 'in_progress'])
    
    def by_priority(self):
        """Retourne les tickets triés par priorité"""
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        return sorted(self.all(), key=lambda t: priority_order.get(t.priority, 4))

