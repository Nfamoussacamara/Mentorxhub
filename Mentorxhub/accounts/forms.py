from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Formulaire personnalisé pour la création d'utilisateur avec email"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Votre adresse email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirmer le mot de passe'})

    def save(self, commit=True):
        """Sauvegarde l'utilisateur avec le rôle depuis request.POST"""
        user = super().save(commit=False)
        # Le rôle sera défini dans la vue avant le save final
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Formulaire personnalisé pour l'authentification avec messages en français"""
    
    error_messages = {
        'invalid_login': "Adresse e-mail ou mot de passe incorrect.",
        'inactive': "Ce compte est désactivé.",
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Votre adresse email'})
        self.fields['password'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Votre mot de passe'})


class RoleSelectionForm(forms.Form):
    """Formulaire pour sélectionner le rôle (mentor ou étudiant)"""
    
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('student', 'Étudiant'),
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        label='Choisissez votre rôle',
        required=True
    )


class UserProfileImageForm(forms.ModelForm):
    """Formulaire pour modifier l'image de profil et la bannière"""
    
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'banner_image']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            'banner_image': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False
        self.fields['banner_image'].required = False
