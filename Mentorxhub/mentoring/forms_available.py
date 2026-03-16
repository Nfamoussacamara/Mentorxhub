from django import forms
from .models import MentoringSession, MentorProfile, StudentProfile

class AvailableSessionForm(forms.ModelForm):
    """
    Formulaire pour créer une session ouverte (sans étudiant assigné).
    Utilisé par les mentors pour créer des créneaux disponibles.
    """
    class Meta:
        model = MentoringSession
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'meeting_link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Session Python Débutant'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le contenu de cette session...'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lien Jitsi/Zoom (optionnel)'
            })
        }
        labels = {
            'title': 'Titre de la session',
            'description': 'Description',
            'date': 'Date',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
            'meeting_link': 'Lien de réunion'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if date and start_time and end_time:
            from datetime import datetime, date as dt_date
            
            if date < dt_date.today():
                raise forms.ValidationError("La date ne peut pas être dans le passé.")
            
            if start_time >= end_time:
                raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")
        
        return cleaned_data
