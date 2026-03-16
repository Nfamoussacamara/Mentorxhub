# Implémentation Google OAuth - MentorXHub

## 📋 Objectif

Ajouter un bouton "Continuer avec Google" sur les pages de connexion et d'inscription pour permettre aux utilisateurs de s'authentifier rapidement avec leur compte Google.

---

## 🎯 Avantages

✅ **Inscription rapide** : Pas besoin de remplir un long formulaire  
✅ **Sécurité** : Authentification gérée par Google  
✅ **Confiance** : Les utilisateurs font confiance à Google  
✅ **Conversion** : Taux d'inscription plus élevé  
✅ **Données vérifiées** : Email vérifié automatiquement

---

## 🛠️ Solution : django-allauth

**django-allauth** est la bibliothèque standard pour l'authentification sociale dans Django.

### Fonctionnalités :
- Support de 50+ providers (Google, Facebook, GitHub, etc.)
- Gestion automatique des emails
- Compatible avec Django 5.x
- Bien maintenue et documentée

---

## 📦 Étape 1 : Installation

### 1.1 Installer django-allauth

```bash
pip install django-allauth
```

### 1.2 Sauvegarder dans requirements.txt

```bash
pip freeze > requirements.txt
```

---

## ⚙️ Étape 2 : Configuration Django

### 2.1 Modifier `settings.py`

**Fichier** : `mentorxhub/settings.py`

Ajoutez les apps nécessaires dans `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps django-allauth
    'django.contrib.sites',  # ← AJOUTER
    'allauth',               # ← AJOUTER
    'allauth.account',       # ← AJOUTER
    'allauth.socialaccount', # ← AJOUTER
    'allauth.socialaccount.providers.google',  # ← AJOUTER
    
    # Vos apps
    'core',
    'accounts',
    'mentoring',
]
```

Ajoutez le SITE_ID (requis par django-allauth) :

```python
# Site ID pour django-allauth
SITE_ID = 1
```

Ajoutez les backends d'authentification :

```python
AUTHENTICATION_BACKENDS = [
    # Backend Django par défaut
    'django.contrib.auth.backends.ModelBackend',
    
    # Backend allauth pour OAuth
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

Configuration allauth :

```python
# Configuration django-allauth
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Connexion par email
ACCOUNT_EMAIL_REQUIRED = True            # Email obligatoire
ACCOUNT_USERNAME_REQUIRED = False        # Pas de username
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Vérification email optionnelle
SOCIALACCOUNT_AUTO_SIGNUP = True         # Création auto du compte
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none' # Pas de vérif pour OAuth

# Redirection après connexion Google
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Configuration spécifique Google
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': 'VOTRE_CLIENT_ID_GOOGLE',
            'secret': 'VOTRE_SECRET_GOOGLE',
            'key': ''
        }
    }
}
```

> **Note** : Nous allons obtenir `client_id` et `secret` à l'étape suivante.

---

## 🔑 Étape 3 : Créer les Credentials Google

### 3.1 Accéder à Google Cloud Console

1. Allez sur : https://console.cloud.google.com/
2. Connectez-vous avec votre compte Google

### 3.2 Créer un Nouveau Projet

1. Cliquez sur le sélecteur de projet (en haut)
2. Cliquez sur **"Nouveau projet"**
3. Nom du projet : `MentorXHub`
4. Cliquez sur **"Créer"**

### 3.3 Activer l'API Google+

1. Dans le menu hamburger (☰), allez dans **"APIs & Services"** → **"Bibliothèque"**
2. Recherchez **"Google+ API"**
3. Cliquez dessus et cliquez sur **"Activer"**

### 3.4 Créer les Credentials OAuth 2.0

1. Allez dans **"APIs & Services"** → **"Credentials"**
2. Cliquez sur **"Créer des identifiants"** → **"ID client OAuth"**
3. Si demandé, configurez l'écran de consentement :
   - Type d'utilisateur : **Externe**
   - Nom de l'application : `MentorXHub`
   - Email de support : votre email
   - Domaine autorisé : `localhost` (pour dev)
   - Cliquez sur **"Enregistrer et continuer"**

4. Type d'application : **Application Web**
5. Nom : `MentorXHub Web Client`
6. **Origines JavaScript autorisées** :
   ```
   http://localhost:8000
   http://127.0.0.1:8000
   ```
7. **URI de redirection autorisés** :
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
8. Cliquez sur **"Créer"**

### 3.5 Récupérer les Credentials

Une popup s'affiche avec :
- **ID client** : `123456789-abcdefg.apps.googleusercontent.com`
- **Secret client** : `GOCSPX-xxxxxxxxxxxxxxxx`

**IMPORTANT** : Copiez-les dans un endroit sûr !

---

## 🔐 Étape 4 : Stocker les Credentials de Manière Sécurisée

### 4.1 Créer un fichier `.env`

**Fichier** : `.env` (à la racine du projet)

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxx
```

### 4.2 Ajouter `.env` au `.gitignore`

**Fichier** : `.gitignore`

```
# Environnement
.env
*.env
```

### 4.3 Installer python-decouple

```bash
pip install python-decouple
pip freeze > requirements.txt
```

### 4.4 Modifier `settings.py`

En haut du fichier :

```python
from pathlib import Path
from decouple import config  # ← AJOUTER
```

Remplacer dans la configuration Google :

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}
```

---

## 🌐 Étape 5 : Configurer les URLs

### 5.1 Modifier `mentorxhub/urls.py`

**Fichier** : `mentorxhub/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('mentoring/', include('mentoring.urls')),
    
    # URLs django-allauth
    path('accounts/', include('allauth.urls')),  # ← AJOUTER
]
```

> **Note** : L'ordre est important. Mettez `allauth.urls` APRÈS `accounts.urls`.

---

## 🗄️ Étape 6 : Migrations de Base de Données

Django-allauth a besoin de créer ses tables.

```bash
python manage.py migrate
```

Vous devriez voir :

```
Running migrations:
  Applying account.0001_initial... OK
  Applying account.0002_email_max_length... OK
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
  Applying socialaccount.0001_initial... OK
  ...
```

---

## 🎨 Étape 7 : Ajouter le Bouton Google au Template

### 7.1 Page de Signup

**Fichier** : `templates/accounts/signup.html`

Ajoutez le bouton Google **avant** le formulaire classique :

```django
{% load socialaccount %}

<div class="login-container">
    <div class="login-header">
        <h2>Créer un compte</h2>
        <p>Rejoignez MentorXHub</p>
    </div>

    <!-- Bouton Google OAuth -->
    <div class="social-login">
        <a href="{% provider_login_url 'google' %}" class="google-btn">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M19.6 10.227c0-.709-.064-1.39-.182-2.045H10v3.868h5.382a4.6 4.6 0 01-1.996 3.018v2.51h3.232c1.891-1.742 2.982-4.305 2.982-7.35z" fill="#4285F4"/>
                <path d="M10 20c2.7 0 4.964-.895 6.618-2.423l-3.232-2.509c-.895.6-2.04.955-3.386.955-2.605 0-4.81-1.76-5.595-4.123H1.064v2.59A9.996 9.996 0 0010 20z" fill="#34A853"/>
                <path d="M4.405 11.9c-.2-.6-.314-1.24-.314-1.9 0-.66.114-1.3.314-1.9V5.51H1.064A9.996 9.996 0 000 10c0 1.614.386 3.14 1.064 4.49l3.34-2.59z" fill="#FBBC05"/>
                <path d="M10 3.977c1.468 0 2.786.505 3.823 1.496l2.868-2.868C14.959.99 12.695 0 10 0 6.09 0 2.71 2.24 1.064 5.51l3.34 2.59C5.19 5.736 7.395 3.977 10 3.977z" fill="#EA4335"/>
            </svg>
            <span>Continuer avec Google</span>
        </a>
    </div>

    <!-- Séparateur -->
    <div class="separator">
        <span>OU</span>
    </div>

    <!-- Formulaire classique -->
    <form method="post">
        {% csrf_token %}
        <!-- Vos champs de formulaire -->
    </form>
</div>
```

### 7.2 CSS pour le Bouton Google

Dans le bloc `<style>` de `signup.html` :

```css
/* Bouton Google OAuth */
.social-login {
    margin-bottom: 1.5rem;
}

.google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.875rem 1rem;
    background: #ffffff;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    color: #1F2937;
    text-decoration: none;
    transition: all 0.2s ease;
    cursor: pointer;
}

.google-btn:hover {
    background: #F9FAFB;
    border-color: #D1D5DB;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.google-btn svg {
    flex-shrink: 0;
}

/* Séparateur "OU" */
.separator {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.5rem 0;
    color: #6B7280;
    font-size: 14px;
    font-weight: 500;
}

.separator::before,
.separator::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E5E7EB;
}

.separator span {
    padding: 0 1rem;
}
```

### 7.3 Pour la Page de Login

Même chose dans `templates/accounts/login.html` si vous voulez permettre la connexion via Google.

---

## 🔄 Étape 8 : Gérer la Création de Compte Personnalisée

Par défaut, django-allauth crée un compte basique. Si vous avez des champs personnalisés (comme `role` dans MentorXHub), vous devez configurer un signal.

### 8.1 Créer un fichier `signals.py`

**Fichier** : `accounts/signals.py`

```python
from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.account.signals import user_signed_up
from .models import CustomUser

@receiver(pre_social_login)
def populate_profile(sender, request, sociallogin, **kwargs):
    """
    Populer les informations du profil lors de la connexion Google
    """
    # Récupérer les données Google
    data = sociallogin.account.extra_data
    user = sociallogin.user
    
    # Si c'est une nouvelle inscription
    if not user.pk:
        # Remplir les infos de base
        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        user.email = data.get('email', '')

@receiver(user_signed_up)
def set_default_role(sender, request, user, **kwargs):
    """
    Définir un rôle par défaut pour les utilisateurs Google OAuth
    """
    # Vérifier si c'est une connexion sociale
    sociallogin = kwargs.get('sociallogin', None)
    
    if sociallogin:
        # Définir le rôle par défaut (STUDENT)
        if not user.role:
            user.role = CustomUser.STUDENT
            user.save()
```

### 8.2 Charger les Signals

**Fichier** : `accounts/apps.py`

```python
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # ← AJOUTER
```

---

## 🧪 Étape 9 : Tester l'Implémentation

### 9.1 Lancer le Serveur

```bash
python manage.py runserver
```

### 9.2 Tester le Flow

1. Allez sur : `http://127.0.0.1:8000/accounts/signup/`
2. Cliquez sur **"Continuer avec Google"**
3. Choisissez un compte Google
4. Acceptez les permissions
5. Vous devriez être redirigé vers la page d'accueil
6. Vérifiez dans l'admin Django que le compte a été créé

### 9.3 Vérifications

✅ Le compte est créé avec l'email Google  
✅ Le prénom et nom sont remplis  
✅ Le rôle est défini (STUDENT par défaut)  
✅ L'utilisateur est automatiquement connecté

---

## 🚀 Étape 10 : Production

### 10.1 Mettre à Jour les Credentials Google

Quand vous déployez :

1. Retournez sur Google Cloud Console
2. Ajoutez vos URLs de production :
   ```
   https://mentorxhub.com
   https://mentorxhub.com/accounts/google/login/callback/
   ```

### 10.2 Variables d'Environnement

Sur votre serveur de production (Heroku, AWS, etc.), définissez :

```bash
GOOGLE_CLIENT_ID=votre_client_id_prod
GOOGLE_CLIENT_SECRET=votre_secret_prod
```

---

## 🎨 Design Bonus : Bouton Moderne

Si vous voulez un design encore plus moderne :

```css
.google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    padding: 0.875rem 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    color: #1F2937;
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.google-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(66, 133, 244, 0.1), transparent);
    transition: left 0.5s ease;
}

.google-btn:hover::before {
    left: 100%;
}

.google-btn:hover {
    background: #ffffff;
    border-color: #4285F4;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(66, 133, 244, 0.15);
}

.google-btn:active {
    transform: translateY(0);
}
```

---

## 📋 Checklist Finale

- [ ] django-allauth installé
- [ ] settings.py configuré
- [ ] Credentials Google créés
- [ ] `.env` créé avec les credentials
- [ ] python-decouple installé
- [ ] URLs configurées
- [ ] Migrations exécutées
- [ ] Bouton ajouté au template
- [ ] CSS appliqué
- [ ] Signals créés pour le rôle
- [ ] Testé en local
- [ ] URLs de production configurées (quand applicable)

---

## 🐛 Troubleshooting

### Erreur : "redirect_uri_mismatch"
**Solution** : Vérifiez que l'URI dans Google Cloud Console correspond exactement à :
```
http://127.0.0.1:8000/accounts/google/login/callback/
```

### Le compte n'a pas de rôle
**Solution** : Vérifiez que les signals sont bien chargés dans `apps.py`.

### "Site matching query does not exist"
**Solution** : Allez dans l'admin Django (`/admin/`) → Sites → Modifiez le site par défaut :
- Domain name: `127.0.0.1:8000`
- Display name: `MentorXHub Local`

---

**Date de création** : 2025-12-01  
**Prochaine étape** : Tester et déployer
