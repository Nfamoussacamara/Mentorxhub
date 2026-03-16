"""
Forms pour le dashboard MentorXHub
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import (
    UserProfile, DashboardSettings, Course, Lesson, 
    Payment, SupportTicket, Message, Conversation
)

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    """Formulaire pour le profil utilisateur"""
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'banner', 'linkedin_url', 'github_url',
            'twitter_url', 'website_url', 'country', 'city', 'timezone',
            'language', 'currency'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous de vous...'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/...'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/...'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/...'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://votresite.com'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pays'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'timezone': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class DashboardSettingsForm(forms.ModelForm):
    """Formulaire pour les paramètres du dashboard"""
    class Meta:
        model = DashboardSettings
        fields = [
            'theme', 'sidebar_collapsed', 'language',
            'email_notifications', 'push_notifications',
            'message_notifications', 'session_reminders',
            'profile_public', 'show_email', 'show_activity'
        ]
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'sidebar_collapsed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'message_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'session_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_activity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CourseForm(forms.ModelForm):
    """Formulaire pour créer/modifier un cours"""
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'short_description', 'thumbnail',
            'difficulty', 'duration_hours', 'price', 'is_published', 'is_free'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du cours'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Description complète du cours'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Description courte (max 500 caractères)'
            }),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.01,
                'min': 0
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LessonForm(forms.ModelForm):
    """Formulaire pour créer/modifier une leçon"""
    class Meta:
        model = Lesson
        fields = [
            'title', 'description', 'content', 'video_url',
            'duration_minutes', 'order', 'is_free'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la leçon'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la leçon'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Contenu de la leçon (HTML/Markdown)'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de la vidéo'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SupportTicketForm(forms.ModelForm):
    """Formulaire pour créer un ticket de support"""
    class Meta:
        model = SupportTicket
        fields = ['category', 'priority', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du ticket'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Décrivez votre problème en détail...'
            }),
        }


class MessageForm(forms.ModelForm):
    """Formulaire pour envoyer un message"""
    class Meta:
        model = Message
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tapez votre message...'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,application/pdf,.doc,.docx'
            }),
        }


class PaymentForm(forms.ModelForm):
    """Formulaire pour les paiements"""
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount', 'currency', 'payment_method']
        widgets = {
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.01,
                'min': 0
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

