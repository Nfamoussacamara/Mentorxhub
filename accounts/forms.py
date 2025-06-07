from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email',
            'autocomplete': 'email'
        })
    )
    first_name = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom',
            'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom',
            'autocomplete': 'family-name'
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-password',
            'placeholder': 'Mot de passe',
            'autocomplete': 'new-password',
            'id': 'id_password1'
        })
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control input-password',
            'placeholder': 'Confirmez votre mot de passe',
            'autocomplete': 'new-password',
            'id': 'id_password2'
        })
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Choisissez votre rôle'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprimer les textes d'aide
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Ajouter des messages d'erreur personnalisés
        self.fields['password1'].error_messages = {
            'required': 'Le mot de passe est requis.',
            'password_too_short': 'Le mot de passe doit contenir au moins 8 caractères.',
            'password_too_common': 'Ce mot de passe est trop courant.',
            'password_entirely_numeric': 'Le mot de passe ne peut pas être entièrement numérique.',
        }
        self.fields['password2'].error_messages = {
            'required': 'La confirmation du mot de passe est requise.',
            'password_mismatch': 'Les deux mots de passe ne correspondent pas.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user