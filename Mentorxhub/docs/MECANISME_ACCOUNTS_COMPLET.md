# 🔐 Mécanisme Complet de l'Application Accounts

## 📋 Vue d'ensemble

L'application `accounts` gère toute l'authentification, l'inscription, la gestion des utilisateurs et le processus d'onboarding de MentorXHub. Elle utilise un modèle utilisateur personnalisé (`CustomUser`) sans username, uniquement avec email.

**Date** : 2025-12-11  
**Version** : 1.0  
**Statut** : ✅ Production

---

## 🏗️ Architecture Globale

### Composants Principaux

```
accounts/
├── models.py              # CustomUser (modèle utilisateur personnalisé)
├── forms.py              # Formulaires d'inscription et connexion
├── views/
│   ├── auth.py          # Login, Signup, Logout
│   ├── profile.py       # Gestion du profil
│   └── onboarding/
│       └── role_selection.py  # Sélection de rôle
├── middleware.py         # OnboardingMiddleware (redirection automatique)
├── adapters.py           # Adapters django-allauth (OAuth Google)
├── signals.py           # Création automatique de profils
└── services/
    └── role_transition.py  # Service de transition de rôle
```

---

## 👤 Modèle CustomUser

### Caractéristiques Principales

```python
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Identifiant unique : EMAIL (pas de username)
    email = models.EmailField(unique=True)
    
    # Informations personnelles
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=[('mentor', 'Mentor'), ('student', 'Étudiant')])
    
    # Profil
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    banner_image = models.ImageField(upload_to='banners/')
    
    # État
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    onboarding_completed = models.BooleanField(default=False)
    
    # Dates
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
```

### Points Clés

1. **Email comme identifiant unique** : `USERNAME_FIELD = 'email'`
2. **Pas de username** : Simplification de l'authentification
3. **Rôle optionnel** : Peut être `None` au début (défini lors de l'onboarding)
4. **Onboarding flag** : `onboarding_completed` pour suivre le processus

---

## 🔄 Flux d'Authentification

### 1. Inscription Classique (Email/Password)

#### Étape 1 : Formulaire d'inscription
```
Utilisateur → /accounts/signup/
    ↓
SignUpView (CreateView)
    ↓
CustomUserCreationForm
    ↓
Validation des données
```

#### Étape 2 : Création de l'utilisateur
```python
# accounts/views/auth.py
def form_valid(self, form):
    user = form.save()  # Crée CustomUser
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(self.request, user)  # Connexion automatique
    return redirect('dashboard:dashboard')
```

#### Étape 3 : Signal post_save
```python
# accounts/signals.py
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance, ...)
        elif instance.role == 'mentor':
            MentorProfile.objects.create(user=instance, ...)
```

#### Étape 4 : Redirection
- Si `role` est défini → Dashboard
- Si `role` est `None` → Onboarding (via middleware)

---

### 2. Connexion Classique (Email/Password)

#### Étape 1 : Formulaire de connexion
```
Utilisateur → /accounts/login/
    ↓
CustomLoginView (LoginView)
    ↓
CustomAuthenticationForm
    ↓
Authentification avec email/password
```

#### Étape 2 : Authentification
```python
# accounts/views/auth.py
def form_valid(self, form):
    email = form.cleaned_data.get('username')  # Email dans le champ username
    password = form.cleaned_data.get('password')
    user = authenticate(username=email, password=password)
    
    if user:
        login(self.request, user)
        return redirect('dashboard:dashboard')
```

#### Étape 3 : Support HTMX
- Détection de `HX-Request` header
- Redirection via `HX-Redirect` pour HTMX
- Fallback classique pour navigation normale

---

### 3. Authentification Google OAuth

#### Étape 1 : Clic sur "Se connecter avec Google"
```
Utilisateur → /accounts/google/login/
    ↓
django-allauth intercepte
    ↓
Redirection vers Google OAuth
```

#### Étape 2 : Callback Google
```
Google → /accounts/google/callback/
    ↓
SocialAccountAdapter.pre_social_login()
    ↓
Vérification si utilisateur existe déjà
    ↓
Si oui → Liaison du compte Google
Si non → Création automatique
```

#### Étape 3 : Création automatique (SocialAccountAdapter)
```python
# accounts/adapters.py
def populate_user(self, request, sociallogin, data):
    user = super().populate_user(request, sociallogin, data)
    
    # Rôle par défaut 'student' si non défini
    if not user.role:
        user.role = 'student'
    
    return user
```

#### Étape 4 : Configuration OAuth
```python
# settings.py
SOCIALACCOUNT_LOGIN_ON_GET = True      # Connexion directe, pas de page intermédiaire
SOCIALACCOUNT_AUTO_SIGNUP = True       # Création automatique
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # Pas de vérification email
```

**Résultat** : Utilisateur créé et connecté automatiquement, redirigé vers le dashboard.

---

## 🚦 Middleware d'Onboarding

### Rôle du Middleware

Le `OnboardingMiddleware` intercepte **toutes les requêtes** et vérifie si l'utilisateur a complété son onboarding.

### Logique de Redirection

```python
# accounts/middleware.py
def __call__(self, request):
    # 1. Ignorer les URLs publiques
    if path.startswith('/static/') or path.startswith('/media/'):
        return self.get_response(request)
    
    # 2. Vérifier l'authentification
    if not request.user.is_authenticated:
        return self.get_response(request)
    
    user = request.user
    
    # 3. Vérification du Rôle
    if not user.role:
        return redirect('accounts:onboarding_role')
    
    # 4. Vérification Onboarding
    if not user.onboarding_completed:
        if user.role == 'student':
            return redirect('mentoring:mentee_onboarding')
        elif user.role == 'mentor':
            return redirect('mentoring:mentor_onboarding')
    
    return self.get_response(request)
```

### URLs Exemptées

Le middleware ignore certaines URLs pour éviter les boucles infinies :

```python
PUBLIC_URLS = [
    '/accounts/login/',
    '/accounts/signup/',
    '/accounts/logout/',
    '/accounts/google/',
    '/admin/',
    '/static/',
    '/media/',
]

ONBOARDING_URLS = [
    '/onboarding/role/',
    '/onboarding/profile/',
]
```

### Flux Complet

```
Utilisateur authentifié
    ↓
Middleware vérifie user.role
    ↓
Si role == None
    → Redirection vers /accounts/onboarding/role/
    ↓
Utilisateur sélectionne un rôle
    ↓
Middleware vérifie onboarding_completed
    ↓
Si onboarding_completed == False
    → Redirection vers onboarding selon le rôle
    ↓
Utilisateur complète l'onboarding
    ↓
onboarding_completed = True
    ↓
Accès libre au dashboard
```

---

## 🎯 Processus d'Onboarding

### Étape 1 : Sélection du Rôle

**URL** : `/accounts/onboarding/role/`  
**Vue** : `RoleSelectionView`

```python
# accounts/views/onboarding/role_selection.py
class RoleSelectionView(TemplateView):
    def post(self, request):
        role = request.POST.get('role')
        if role in ['mentor', 'student']:
            request.user.role = role
            request.user.save()
            return redirect('dashboard:dashboard')
```

**Fonctionnalités** :
- Affichage de deux boutons : "Je suis un Mentor" / "Je suis un Étudiant"
- Sauvegarde du rôle dans `CustomUser.role`
- Redirection vers le dashboard (middleware redirigera vers l'onboarding spécifique)

---

### Étape 2 : Onboarding selon le Rôle

#### Pour les Étudiants (Mentorés)

**URL** : `/mentoring/onboarding/mentee/`  
**Vue** : `MenteeOnboardingView`

**Champs à remplir** :
- Niveau (débutant, intermédiaire, avancé)
- Objectifs d'apprentissage
- Intérêts
- Langues préférées
- Profil GitHub (optionnel)

**Après soumission** :
- `StudentProfile` mis à jour
- `onboarding_completed = True`
- Accès au dashboard étudiant

#### Pour les Mentors

**URL** : `/mentoring/onboarding/mentor/`  
**Vue** : `MentorOnboardingView`

**Champs à remplir** :
- Domaine d'expertise
- Années d'expérience
- Tarif horaire
- Langues parlées
- Certifications
- Profils LinkedIn/GitHub/Website

**Après soumission** :
- `MentorProfile` créé avec `status='pending'`
- `onboarding_completed = True`
- Accès au dashboard mentor (en attente d'approbation)

---

## 🔄 Transition de Rôle

### Service de Transition

Le service `RoleTransitionService` permet à un étudiant de demander à devenir mentor.

#### 1. Demande de Transition

```python
# accounts/services/role_transition.py
def request_mentorship(user: CustomUser) -> MentorProfile:
    """
    Permet à un étudiant de demander à devenir mentor.
    Crée un profil mentor 'pending' sans changer le rôle user.
    """
    if user.role == 'mentor':
        raise ValidationError("L'utilisateur est déjà un mentor.")
    
    # Créer le profil mentor en attente
    profile = MentorProfile.objects.create(
        user=user,
        status='pending',
        expertise='À définir',
        years_of_experience=0,
        hourly_rate=0.0,
        languages='À définir'
    )
    return profile
```

**Important** : Le rôle `user.role` reste `'student'` jusqu'à l'approbation.

#### 2. Approbation par un Admin

```python
def approve_mentorship(user: CustomUser, admin_user: CustomUser) -> CustomUser:
    """
    Valide la transition d'un utilisateur vers le rôle mentor.
    Change le rôle de l'utilisateur et approuve le profil.
    """
    if not admin_user.is_staff:
        raise ValidationError("Seul un administrateur peut valider.")
    
    with transaction.atomic():
        # 1. Approuver le profil
        profile.status = 'approved'
        profile.save()
        
        # 2. Changer le rôle utilisateur
        user.role = 'mentor'
        user.save()
    
    return user
```

**Résultat** : L'utilisateur devient officiellement mentor avec accès aux fonctionnalités mentors.

---

## 🔌 Adapters django-allauth

### AccountAdapter (Inscription Classique)

```python
# accounts/adapters.py
class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Sauvegarde l'utilisateur avec les données du formulaire.
        La logique métier (rôle, etc.) est gérée par le formulaire.
        """
        user = super().save_user(request, user, form, commit=False)
        if commit:
            user.save()
        return user
```

**Rôle** : Minimal, laisse le formulaire gérer la logique.

---

### SocialAccountAdapter (OAuth Google)

```python
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Autorise la création automatique de compte.
        Supprime la page intermédiaire django-allauth.
        """
        return True
    
    def populate_user(self, request, sociallogin, data):
        """
        Remplit les informations utilisateur depuis Google.
        Crée un utilisateur MINIMAL (email, first_name, last_name).
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Rôle par défaut 'student' si non défini
        if not user.role:
            user.role = 'student'
        
        return user
    
    def pre_social_login(self, request, sociallogin):
        """
        Lie automatiquement les comptes existants.
        Si un utilisateur existe avec le même email, on lie le compte Google.
        """
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
```

**Fonctionnalités** :
- ✅ Création automatique sans page intermédiaire
- ✅ Liaison automatique des comptes existants
- ✅ Rôle par défaut 'student'
- ✅ Utilisateur minimal (pas de logique métier complexe)

---

## 📡 Signaux Django

### Création Automatique de Profils

```python
# accounts/signals.py
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil Student ou Mentor
    quand un nouvel utilisateur est créé.
    """
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(
                user=instance,
                level='Débutant',
                learning_goals='À définir',
                interests='À définir',
                preferred_languages='Français'
            )
        elif instance.role == 'mentor':
            MentorProfile.objects.create(
                user=instance,
                expertise='À définir',
                years_of_experience=0,
                hourly_rate=50.00,
                languages='Français'
            )
```

**Déclenchement** : Automatiquement après `user.save()` si `created=True`

**Important** : Le profil est créé avec des valeurs par défaut, à compléter lors de l'onboarding.

---

## 🔐 Configuration Django

### Settings.py

```python
# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'accounts.CustomUser'

# Backends d'authentification
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Adapters personnalisés
ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "accounts.adapters.SocialAccountAdapter"

# Configuration OAuth Google
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# Redirections
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"

# Configuration allauth
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
```

### Middleware

```python
MIDDLEWARE = [
    # ... autres middlewares ...
    'accounts.middleware.OnboardingMiddleware',  # Middleware d'onboarding
]
```

---

## 🔄 Flux Complets

### Flux 1 : Inscription Email/Password

```
1. Utilisateur → /accounts/signup/
2. SignUpView affiche le formulaire
3. Utilisateur remplit email, password, role
4. CustomUser créé avec role défini
5. Signal post_save → Création automatique du profil (StudentProfile ou MentorProfile)
6. Utilisateur connecté automatiquement
7. Redirection vers dashboard
8. Middleware vérifie onboarding_completed
9. Si False → Redirection vers onboarding spécifique
10. Utilisateur complète l'onboarding
11. onboarding_completed = True
12. Accès libre au dashboard
```

### Flux 2 : Connexion Google OAuth

```
1. Utilisateur → /accounts/google/login/
2. Redirection vers Google OAuth
3. Utilisateur autorise l'application
4. Google → /accounts/google/callback/
5. SocialAccountAdapter.pre_social_login()
   - Vérifie si utilisateur existe déjà
   - Si oui → Lie le compte Google
   - Si non → Continue
6. SocialAccountAdapter.populate_user()
   - Crée CustomUser avec email, first_name, last_name
   - Définit role = 'student' par défaut
7. Signal post_save → Création automatique de StudentProfile
8. Utilisateur connecté automatiquement
9. Redirection vers dashboard
10. Middleware vérifie role
11. Si role == None → Redirection vers /accounts/onboarding/role/
12. Utilisateur sélectionne un rôle
13. Middleware vérifie onboarding_completed
14. Si False → Redirection vers onboarding spécifique
15. Utilisateur complète l'onboarding
16. onboarding_completed = True
17. Accès libre au dashboard
```

### Flux 3 : Transition Étudiant → Mentor

```
1. Étudiant connecté
2. Accède à la page de demande de mentorat
3. Appelle RoleTransitionService.request_mentorship(user)
4. MentorProfile créé avec status='pending'
5. user.role reste 'student'
6. Admin reçoit une notification
7. Admin approuve via RoleTransitionService.approve_mentorship(user, admin)
8. MentorProfile.status = 'approved'
9. user.role = 'mentor'
10. Utilisateur devient mentor avec accès aux fonctionnalités mentors
```

---

## 🛡️ Sécurité

### Points de Sécurité

1. **Email unique** : Un seul compte par email
2. **Liaison automatique** : Les comptes Google sont liés aux comptes existants
3. **Validation des rôles** : Transition de rôle nécessite approbation admin
4. **Middleware protection** : Redirection automatique si onboarding incomplet
5. **CSRF protection** : Tous les formulaires protégés
6. **Permissions** : Utilisation de `@login_required` et `is_staff` checks

---

## 📊 Modèles Liés

### StudentProfile (mentoring/models.py)

```python
class StudentProfile(models.Model):
    user = OneToOneField(CustomUser, related_name='student_profile')
    level = CharField(max_length=50)
    learning_goals = TextField()
    interests = CharField(max_length=200)
    preferred_languages = CharField(max_length=200)
    github_profile = URLField()
    total_sessions = PositiveIntegerField(default=0)
```

### MentorProfile (mentoring/models.py)

```python
class MentorProfile(models.Model):
    user = OneToOneField(CustomUser, related_name='mentor_profile')
    expertise = CharField(max_length=100)
    years_of_experience = PositiveIntegerField()
    hourly_rate = DecimalField(max_digits=10, decimal_places=2)
    languages = CharField(max_length=200)
    certifications = TextField()
    rating = DecimalField(max_digits=3, decimal_places=2, default=0.0)
    status = CharField(choices=[('pending', 'En attente'), ('approved', 'Approuvé'), ('rejected', 'Rejeté')])
    is_available = BooleanField(default=True)
```

---

## 🧪 Tests

### Tests Disponibles

- `accounts/tests/test_middleware.py` : Tests du middleware d'onboarding
- `accounts/tests/test_role_transition.py` : Tests de transition de rôle

---

## 📝 Notes Importantes

1. **Pas de username** : L'email est l'identifiant unique
2. **Rôle optionnel** : Peut être `None` au début, défini lors de l'onboarding
3. **Onboarding obligatoire** : Le middleware force la complétion
4. **Profils automatiques** : Création automatique via signaux
5. **OAuth sans page intermédiaire** : Connexion directe avec Google
6. **Transition de rôle** : Nécessite approbation admin

---

## 🔍 Dépannage

### Problème : Boucle de redirection infinie
**Solution** : Vérifier que les URLs d'onboarding sont dans `ONBOARDING_URLS` du middleware

### Problème : Utilisateur créé mais pas de profil
**Solution** : Vérifier que les signaux sont bien enregistrés dans `apps.py`

### Problème : OAuth ne fonctionne pas
**Solution** : Vérifier les credentials Google dans Django Admin → Sites → Social Applications

### Problème : Middleware bloque l'accès
**Solution** : Vérifier que `onboarding_completed = True` après l'onboarding

---

## 📚 Références

- **Documentation Django Auth** : https://docs.djangoproject.com/en/stable/topics/auth/
- **Documentation django-allauth** : https://docs.allauth.org/
- **Custom User Model** : https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model

---

*Document créé le : 2025-12-11*  
*Auteur : Assistant IA*  
*Statut : ✅ Complété et à jour*

