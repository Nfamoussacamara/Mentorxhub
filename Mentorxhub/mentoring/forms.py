from django import forms
from .models import MentorProfile, StudentProfile, Availability, MentoringSession, Subject

class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = [
            'expertise', 'years_of_experience', 'hourly_rate', 'languages',
            'certifications', 'linkedin_profile', 'github_profile', 'website'
        ]
        widgets = {
            'expertise': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre domaine d\'expertise'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Français, Anglais, Python, JavaScript'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Listez vos certifications'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/votre-profil'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/votre-profil'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://votre-site.com'
            })
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['level', 'learning_goals', 'interests', 'preferred_languages', 'github_profile']
        widgets = {
            'level': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('débutant', 'Débutant'),
                ('intermédiaire', 'Intermédiaire'),
                ('avancé', 'Avancé')
            ]),
            'learning_goals': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Décrivez vos objectifs d\'apprentissage'
            }),
            'interests': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Développement Web, Data Science, IA'
            }),
            'preferred_languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Français, Anglais, Python, JavaScript'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/votre-profil'
            })
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_recurring']
        widgets = {
            'day_of_week': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")

        return cleaned_data

class MentoringSessionForm(forms.ModelForm):
    class Meta:
        model = MentoringSession
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'meeting_link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de la session'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description détaillée de la session'
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
                'placeholder': 'Lien de la réunion (Zoom, Meet, etc.)'
            })
        }

class MentorMentoringSessionForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.all(),
        label="Étudiant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MentoringSession
        fields = ['student', 'title', 'description', 'date', 'start_time', 'end_time', 'meeting_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la session'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien de la réunion'})
        }

    def __init__(self, *args, **kwargs):
        mentor = kwargs.pop('mentor', None)
        super().__init__(*args, **kwargs)
        if mentor:
            # On pourrait filtrer ici pour ne montrer que les étudiants ayant déjà eu une session avec ce mentor
            # Mais pour l'instant on montre tous les étudiants actifs
            self.fields['student'].queryset = StudentProfile.objects.filter(user__is_active=True).select_related('user')
            self.fields['student'].label_from_instance = lambda obj: obj.user.get_full_name() or obj.user.email

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

class SessionFeedbackForm(forms.ModelForm):
    class Meta:
        model = MentoringSession
        fields = ['rating', 'feedback']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'type': 'range'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre expérience de la session'
            })
        }

class MenteeOnboardingForm(forms.ModelForm):
    """Formulaire d'onboarding pour les mentorés avec tous les champs optionnels."""
    
    class Meta:
        model = StudentProfile
        fields = ['level', 'learning_goals', 'interests', 'preferred_languages', 'github_profile']
        widgets = {
            'level': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Sélectionnez votre niveau (optionnel)'
            }, choices=[
                ('', 'Sélectionnez votre niveau (optionnel)'),
                ('débutant', 'Débutant'),
                ('intermédiaire', 'Intermédiaire'),
                ('avancé', 'Avancé')
            ]),
            'learning_goals': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Quels sont vos objectifs d\'apprentissage ? (optionnel)'
            }),
            'interests': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox-multiple',
            }),
            'preferred_languages': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Français, Anglais, Python, JavaScript (optionnel)'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://github.com/votre-profil (optionnel)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous les champs non requis
        for field in self.fields.values():
            field.required = False
        
        # Charger les matières depuis la base de données pour le champ interests
        from .models import Subject
        if 'interests' in self.fields:
            self.fields['interests'].queryset = Subject.objects.filter(is_active=True).order_by('name')
            self.fields['interests'].label = "Centres d'intérêt"
            self.fields['interests'].help_text = "Sélectionnez une ou plusieurs matières qui vous intéressent (plusieurs choix possibles)"
            self.fields['interests'].widget.attrs.update({
                'class': 'form-checkbox-multiple'
            })

class MentorOnboardingForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = [
            'expertise', 'years_of_experience', 'hourly_rate', 'languages',
            'linkedin_profile'
        ]
        widgets = {
            'expertise': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre domaine d\'expertise'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'placeholder': 'Années d\'expérience'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Tarif horaire en €'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Français, Anglais, Python, JavaScript'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://linkedin.com/in/votre-profil'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous ces champs obligatoires
        mandatory_fields = ['expertise', 'years_of_experience', 'hourly_rate', 'languages', 'linkedin_profile']
        for field_name in mandatory_fields:
            self.fields[field_name].required = True
 