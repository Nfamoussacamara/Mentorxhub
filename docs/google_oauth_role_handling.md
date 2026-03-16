# Adaptation Google OAuth pour CustomUser avec Rôle Obligatoire

## Problème Identifié

Le modèle `CustomUser` a :
- `role` comme champ **obligatoire** (`REQUIRED_FIELDS`)
- Choix : `'mentor'` ou `'student'`

Lors de l'inscription Google, l'utilisateur ne choisit pas de rôle → **Erreur de création de compte**.

---

## 🎯 Solution 1 : Page de Sélection du Rôle (RECOMMANDÉE)

### Flux Utilisateur :
1. Utilisateur clique sur "Continuer avec Google"
2. Authentification Google réussie
3. **→ Redirection vers page "Choisissez votre rôle"**
4. Utilisateur sélectionne Mentor ou Étudiant
5. Compte créé et connexion

### Avantages :
✅ UX claire et guidée  
✅ Respect du modèle existant  
✅ Collecte d'information importante  
✅ Pas de rôle par défaut arbitraire

---

### Implémentation

#### 1. Créer la Vue de Sélection du Rôle

**Fichier** : `accounts/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def select_role(request):
    """
    Page pour sélectionner le rôle après inscription Google OAuth
    """
    user = request.user
    
    # Si l'utilisateur a déjà un rôle, rediriger
    if user.role:
        return redirect('home')
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        # Validation
        if role not in ['mentor', 'student']:
            messages.error(request, 'Veuillez sélectionner un rôle valide.')
            return render(request, 'accounts/select_role.html')
        
        # Attribuer le rôle
        user.role = role
        user.save()
        
        messages.success(request, f'Bienvenue en tant que {user.get_role_display()} !')
        return redirect('home')
    
    return render(request, 'accounts/select_role.html')
```

#### 2. Créer le Template de Sélection

**Fichier** : `templates/accounts/select_role.html`

```django
{% extends 'base.html' %}
{% load static %}

{% block title %}Choisissez votre rôle - MentorXHub{% endblock %}

{% block extra_css %}
<style>
    #role-selection-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }

    .role-container {
        max-width: 700px;
        width: 100%;
        background: #ffffff;
        padding: 3rem;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    .role-header h1 {
        font-size: 2rem;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }

    .role-header p {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    .role-options {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .role-card {
        position: relative;
        padding: 2rem 1.5rem;
        border: 3px solid #E5E7EB;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        background: #ffffff;
    }

    .role-card:hover {
        border-color: #2563EB;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
    }

    .role-card input[type="radio"] {
        position: absolute;
        opacity: 0;
    }

    .role-card input[type="radio"]:checked ~ .role-content {
        color: #2563EB;
    }

    .role-card input[type="radio"]:checked ~ .role-content .role-icon {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .role-card.selected {
        border-color: #2563EB;
        background: #EFF6FF;
    }

    .role-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 1rem;
        background: #F3F4F6;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        transition: all 0.3s ease;
    }

    .role-content h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }

    .role-content p {
        color: #6B7280;
        font-size: 0.875rem;
        line-height: 1.5;
    }

    .submit-btn {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .submit-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    .submit-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    @media (max-width: 640px) {
        .role-options {
            grid-template-columns: 1fr;
        }
    }
</style>
{% endblock %}

{% block content %}
<div id="role-selection-page">
    <div class="role-container">
        <div class="role-header">
            <h1>Bienvenue sur MentorXHub !</h1>
            <p>Pour continuer, veuillez choisir votre rôle</p>
        </div>

        <form method="post" id="roleForm">
            {% csrf_token %}
            
            <div class="role-options">
                <!-- Carte Mentor -->
                <label class="role-card" for="role-mentor">
                    <input type="radio" name="role" value="mentor" id="role-mentor" required>
                    <div class="role-content">
                        <div class="role-icon">🎓</div>
                        <h3>Je suis Mentor</h3>
                        <p>Je souhaite partager mon expérience et guider des étudiants</p>
                    </div>
                </label>

                <!-- Carte Étudiant -->
                <label class="role-card" for="role-student">
                    <input type="radio" name="role" value="student" id="role-student" required>
                    <div class="role-content">
                        <div class="role-icon">📚</div>
                        <h3>Je suis Étudiant</h3>
                        <p>Je cherche un mentor pour m'accompagner dans mon parcours</p>
                    </div>
                </label>
            </div>

            <button type="submit" class="submit-btn">Continuer</button>
        </form>
    </div>
</div>

<script>
    // Ajouter la classe "selected" à la carte cochée
    document.querySelectorAll('.role-card input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', function() {
            // Enlever "selected" de toutes les cartes
            document.querySelectorAll('.role-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            // Ajouter "selected" à la carte cochée
            if (this.checked) {
                this.closest('.role-card').classList.add('selected');
            }
        });
    });
</script>
{% endblock %}
```

#### 3. Ajouter l'URL

**Fichier** : `accounts/urls.py`

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('select-role/', views.select_role, name='select_role'),  # ← AJOUTER
]
```

#### 4. Modifier le Signal OAuth

**Fichier** : `accounts/signals.py`

```python
from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import user_signed_up
from django.shortcuts import redirect
from .models import CustomUser

@receiver(pre_social_login)
def populate_profile(sender, request, sociallogin, **kwargs):
    """
    Remplir les informations de base depuis Google
    """
    data = sociallogin.account.extra_data
    user = sociallogin.user
    
    if not user.pk:
        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        user.email = data.get('email', '')
        # NE PAS définir le rôle ici

@receiver(user_signed_up)
def redirect_to_role_selection(sender, request, user, **kwargs):
    """
    Créer l'utilisateur SANS rôle pour forcer la sélection
    """
    sociallogin = kwargs.get('sociallogin', None)
    
    if sociallogin:
        # Laisser role à None/vide
        # L'utilisateur sera redirigé vers select_role
        pass
```

#### 5. Modifier `settings.py`

**Ajouter** :

```python
# Redirection après connexion Google
LOGIN_REDIRECT_URL = '/accounts/select-role/'  # ← Vers sélection rôle
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
```

#### 6. Modifier le Modèle (Optionnel)

Si le champ `role` doit être **optionnel temporairement** pour permettre la création :

**Fichier** : `accounts/models.py`

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('student', 'Étudiant'),
    )
    
    email = models.EmailField(_('adresse email'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)  # ← MODIFIER
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # ← ENLEVER 'role'

    def __str__(self):
        return self.email
```

**Migration** :

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🎯 Solution 2 : Rôle par Défaut "Étudiant"

Plus simple mais moins flexible.

**Fichier** : `accounts/signals.py`

```python
@receiver(user_signed_up)
def set_default_student_role(sender, request, user, **kwargs):
    sociallogin = kwargs.get('sociallogin', None)
    
    if sociallogin and not user.role:
        user.role = 'student'  # Rôle par défaut
        user.save()
```

**Avantage** : Inscription immédiate  
**Inconvénient** : Les mentors doivent changer leur rôle manuellement après

---

## 🎯 Solution 3 : Middleware de Protection

Forcer la sélection du rôle avant d'accéder à toute page.

**Fichier** : `accounts/middleware.py`

```python
from django.shortcuts import redirect
from django.urls import reverse

class RoleRequiredMiddleware:
    """
    Rediriger vers la sélection de rôle si l'utilisateur n'en a pas
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Chemins autorisés sans rôle
        allowed_paths = [
            reverse('accounts:select_role'),
            reverse('accounts:logout'),
            '/admin/',
        ]
        
        # Si l'utilisateur est connecté mais n'a pas de rôle
        if request.user.is_authenticated and not request.user.role:
            if request.path not in allowed_paths:
                return redirect('accounts:select_role')
        
        return self.get_response(request)
```

**Dans `settings.py`** :

```python
MIDDLEWARE = [
    # ...
    'accounts.middleware.RoleRequiredMiddleware',  # ← AJOUTER à la fin
]
```

---

## 📋 Recommandation Finale

**Solution 1** (Page de sélection) est la meilleure car :
- ✅ UX claire
- ✅ Collecte d'info essentielle
- ✅ Respect du modèle
- ✅ Flexibilité future (ajouter d'autres infos)

---

**Date** : 2025-12-01
