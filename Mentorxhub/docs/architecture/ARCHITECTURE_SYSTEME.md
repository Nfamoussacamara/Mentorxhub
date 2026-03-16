# 🏗️ Architecture du Système MentorXHub

## 📦 Vue d'Ensemble

**MentorXHub** est une plateforme de mentorat construite avec **Django 6.0** qui connecte des mentors et des étudiants pour des sessions de mentorat.

---

## 🎯 Applications Django

Le projet est organisé en **3 applications principales** :

### 1️⃣ **Core** (`core/`)
**Rôle** : Pages publiques et navigation principale

**Responsabilités** :
- Page d'accueil (`home`)
- Dashboard principal avec redirection automatique
- Pages publiques (tarifs, à propos, blog, etc.)
- Pages légales (politique de confidentialité, conditions)

**Fichiers clés** :
- `views.py` - Vues pour pages publiques et dashboard
- `urls.py` - Routes principales (`/`, `/dashboard/`, `/pricing/`, etc.)
- `templatetags/custom_filters.py` - Filtres personnalisés (split, trim, mul)

**Templates** :
- `home.html` - Page d'accueil
- `core/pricing.html`, `core/about.html`, etc.

---

### 2️⃣ **Accounts** (`accounts/`)
**Rôle** : Gestion des utilisateurs et authentification

**Responsabilités** :
- Modèle utilisateur personnalisé (`CustomUser`)
- Authentification (connexion, inscription, déconnexion)
- Gestion des profils utilisateur
- Onboarding (sélection de rôle)
- OAuth Google (via django-allauth)
- Middleware d'onboarding

**Fichiers clés** :
- `models.py` - `CustomUser` (email, role, bio, profile_picture, banner_image)
- `views/auth.py` - `CustomLoginView`, `SignUpView`, `CustomLogoutView`
- `views/profile.py` - `ProfileDisplayView`, `ProfileEditView`
- `views/onboarding/role.py` - `RoleSelectionView`
- `middleware.py` - `OnboardingMiddleware` (redirection automatique)
- `adapters.py` - Adapters pour django-allauth
- `forms.py` - Formulaires d'authentification et profil

**Templates** :
- `accounts/login.html` - Connexion
- `accounts/signup.html` - Inscription
- `accounts/profile.html` - Affichage profil
- `accounts/profile_edit.html` - Édition profil
- `accounts/onboarding/role_selection.html` - Sélection rôle

**Modèles** :
- `CustomUser` : Utilisateur avec email, rôle (mentor/student), profil

---

### 3️⃣ **Mentoring** (`mentoring/`)
**Rôle** : Fonctionnalités de mentorat

**Responsabilités** :
- Gestion des profils mentor et étudiant
- Liste et recherche de mentors
- Gestion des disponibilités
- Sessions de mentorat
- Onboarding mentor/étudiant
- Feedback et évaluations

**Fichiers clés** :
- `models.py` - `MentorProfile`, `StudentProfile`, `Availability`, `MentoringSession`
- `views/main.py` - Vues principales (liste mentors, profils, sessions)
- `views/onboarding/` - Formulaires d'onboarding
- `forms.py` - Formulaires de mentorat
- `urls.py` - Routes mentorat (`/mentoring/mentors/`, `/mentoring/sessions/`, etc.)

**Templates** :
- `mentoring/mentors_list.html` - Liste des mentors
- `mentoring/mentor_public_profile.html` - Profil public mentor
- `mentoring/session_form.html` - Formulaire de session
- `mentoring/onboarding/mentor_form.html` - Onboarding mentor
- `mentoring/onboarding/mentee_form.html` - Onboarding étudiant

**Modèles** :
- `MentorProfile` : Profil mentor (expertise, tarif, langues, disponibilités)
- `StudentProfile` : Profil étudiant (niveau, objectifs, langues préférées)
- `Availability` : Disponibilités des mentors
- `MentoringSession` : Sessions de mentorat (date, heure, statut, feedback)

---

## 🔄 Flux de Fonctionnement

### 1. **Inscription / Connexion**

```
Utilisateur → /accounts/signup/ ou /accounts/login/
    ↓
Authentification réussie
    ↓
Redirection → /dashboard/
    ↓
Middleware vérifie le rôle
    ↓
Si pas de rôle → /accounts/onboarding/role/
    ↓
Sélection du rôle (mentor ou student)
    ↓
Redirection → /dashboard/
```

### 2. **Dashboard Principal**

```
/dashboard/ → core/views.py → dashboard()
    ↓
Vérification du rôle
    ↓
Si mentor → mentor_dashboard() → dashboard-mentor.html
Si étudiant → student_dashboard() → dashboard-mentee.html
Si pas de rôle → redirect('accounts:onboarding_role')
```

### 3. **Onboarding**

```
Sélection du rôle → /accounts/onboarding/role/
    ↓
Création du profil (MentorProfile ou StudentProfile)
    ↓
Redirection → /mentoring/onboarding/mentor/ ou /mentee/
    ↓
Formulaire d'onboarding
    ↓
Redirection → /dashboard/
```

### 4. **Sessions de Mentorat**

```
Étudiant → /mentoring/mentors/ → Liste des mentors
    ↓
Sélection d'un mentor → /mentoring/mentor/<id>/
    ↓
Création de session → /mentoring/sessions/create/<mentor_id>/
    ↓
Session créée → /mentoring/sessions/<id>/
    ↓
Après session → /mentoring/sessions/<id>/feedback/
```

---

## 🗂️ Structure des Modèles

### **CustomUser** (accounts/models.py)
```
- email (unique)
- first_name, last_name
- role (mentor/student)
- bio
- profile_picture
- banner_image
- onboarding_completed
```

### **MentorProfile** (mentoring/models.py)
```
- user (OneToOne → CustomUser)
- expertise
- years_of_experience
- hourly_rate
- languages
- rating
- total_sessions
- status (pending/approved/rejected)
- is_available
```

### **StudentProfile** (mentoring/models.py)
```
- user (OneToOne → CustomUser)
- level
- learning_goals
- interests
- preferred_languages
- github_profile
- total_sessions
```

### **MentoringSession** (mentoring/models.py)
```
- mentor (ForeignKey → MentorProfile)
- student (ForeignKey → StudentProfile)
- title, description
- date, start_time, end_time
- status (scheduled/in_progress/completed/cancelled)
- meeting_link
- rating, feedback
```

### **Availability** (mentoring/models.py)
```
- mentor (ForeignKey → MentorProfile)
- day_of_week
- start_time, end_time
- is_recurring
```

---

## 🔐 Système d'Authentification

### **Backends**
1. **Django ModelBackend** - Authentification email/password
2. **Allauth Backend** - OAuth Google

### **Méthodes de Connexion**
- Email + Mot de passe
- Google OAuth (via django-allauth)

### **Middleware**
- `OnboardingMiddleware` : Vérifie le rôle et l'état d'onboarding
- Redirige automatiquement vers les pages appropriées

---

## 📁 Structure des Fichiers

```
Mentorxhub/
├── accounts/              # Application Accounts
│   ├── models.py          # CustomUser
│   ├── views/
│   │   ├── auth.py        # Login, Signup, Logout
│   │   ├── profile.py     # Profil utilisateur
│   │   └── onboarding/    # Sélection de rôle
│   ├── middleware.py      # OnboardingMiddleware
│   ├── adapters.py        # Allauth adapters
│   ├── forms.py           # Formulaires
│   └── templates/         # Templates accounts
│
├── core/                  # Application Core
│   ├── views.py           # Pages publiques + Dashboard
│   ├── urls.py            # Routes principales
│   ├── templatetags/      # Filtres personnalisés
│   └── templates/         # Templates core
│
├── mentoring/             # Application Mentoring
│   ├── models.py          # MentorProfile, StudentProfile, etc.
│   ├── views/
│   │   ├── main.py        # Vues principales
│   │   └── onboarding/    # Onboarding mentor/étudiant
│   ├── forms.py           # Formulaires mentorat
│   ├── urls.py            # Routes mentorat
│   └── templates/         # Templates mentoring
│
├── mentorxhub/            # Configuration projet
│   ├── settings.py        # Configuration Django
│   └── urls.py            # URLs racine
│
└── templates/             # Templates globaux
    ├── base.html          # Template de base
    ├── home.html          # Page d'accueil
    ├── dashboard-mentor.html
    └── dashboard-mentee.html
```

---

## 🔗 Routage des URLs

### **URLs Racine** (`mentorxhub/urls.py`)
```
/ → core.urls
/accounts/ → accounts.urls + allauth.urls
/mentoring/ → mentoring.urls
/admin/ → Django admin
```

### **Core URLs** (`core/urls.py`)
```
/ → home
/dashboard/ → dashboard (redirige selon rôle)
/pricing/ → pricing_view
/top-mentors/ → top_mentors_view
/about/ → about_view
...
```

### **Accounts URLs** (`accounts/urls.py`)
```
/accounts/signup/ → SignUpView
/accounts/login/ → CustomLoginView
/accounts/logout/ → CustomLogoutView
/accounts/profile/ → ProfileDisplayView
/accounts/profile/edit/ → ProfileEditView
/accounts/onboarding/role/ → RoleSelectionView
...
```

### **Mentoring URLs** (`mentoring/urls.py`)
```
/mentoring/mentors/ → MentorListView
/mentoring/mentor/<id>/ → PublicMentorProfileView
/mentoring/sessions/ → MentoringSessionListView
/mentoring/sessions/create/<mentor_id>/ → MentoringSessionCreateView
/mentoring/onboarding/mentor/ → MentorOnboardingView
/mentoring/onboarding/mentee/ → MenteeOnboardingView
...
```

---

## 🎨 Système de Templates

### **Template de Base** (`templates/base.html`)
- Navbar moderne avec menu utilisateur
- Footer avec liens
- Support des messages Django
- Blocs : `content`, `extra_css`, `extra_js`

### **Templates par Application**

**Core** :
- `home.html` - Page d'accueil
- `core/pricing.html` - Tarifs
- `core/about.html` - À propos
- etc.

**Accounts** :
- `accounts/login.html` - Connexion
- `accounts/signup.html` - Inscription
- `accounts/profile.html` - Profil (moderne avec bannière)
- `accounts/profile_edit.html` - Édition profil

**Mentoring** :
- `mentoring/mentors_list.html` - Liste mentors
- `mentoring/mentor_public_profile.html` - Profil public
- `mentoring/session_form.html` - Formulaire session
- etc.

**Dashboards** :
- `dashboard-mentor.html` - Dashboard mentor
- `dashboard-mentee.html` - Dashboard étudiant

---

## 🎯 Flux Utilisateur Principal

### **Nouvel Utilisateur**
```
1. Inscription → /accounts/signup/
2. Connexion automatique
3. Redirection → /dashboard/
4. Middleware détecte : pas de rôle
5. Redirection → /accounts/onboarding/role/
6. Sélection : Mentor ou Étudiant
7. Création du profil (MentorProfile ou StudentProfile)
8. Redirection → /mentoring/onboarding/mentor/ ou /mentee/
9. Formulaire d'onboarding
10. Redirection → /dashboard/
11. Dashboard affiché selon le rôle
```

### **Utilisateur Existant (Mentor)**
```
1. Connexion → /accounts/login/
2. Redirection → /dashboard/
3. Dashboard détecte : role = 'mentor'
4. Affichage → dashboard-mentor.html
5. Statistiques : demandes, sessions, note, revenus
6. Sessions à venir avec étudiants
```

### **Utilisateur Existant (Étudiant)**
```
1. Connexion → /accounts/login/
2. Redirection → /dashboard/
3. Dashboard détecte : role = 'student'
4. Affichage → dashboard-mentee.html
5. Statistiques : heures, sessions, mentors actifs
6. Sessions à venir avec mentors
7. Mentors recommandés
```

---

## 🔧 Composants Techniques

### **Middleware Personnalisé**
- `OnboardingMiddleware` : Gère le flux d'onboarding automatique

### **Signals Django**
- Création automatique de profils lors de la sélection de rôle

### **Filtres Template Personnalisés**
- `split` : Diviser une chaîne
- `trim` : Supprimer les espaces
- `mul` : Multiplier deux valeurs

### **Formulaires**
- Réutilisation des formulaires d'onboarding pour l'édition de profil
- Formulaires d'images pour profil et bannière

---

## 📊 Base de Données

### **Relations**
```
CustomUser (1) ←→ (1) MentorProfile
CustomUser (1) ←→ (1) StudentProfile
MentorProfile (1) ←→ (N) Availability
MentorProfile (1) ←→ (N) MentoringSession
StudentProfile (1) ←→ (N) MentoringSession
```

### **Base de Données**
- SQLite (développement) : `db.sqlite3`
- Prêt pour PostgreSQL/MySQL en production

---

## 🎨 Design System

### **Styles**
- Design moderne avec glassmorphism
- Gradients (night blue → indigo → purple)
- Animations fluides
- Responsive mobile-first

### **Fichiers CSS Principaux**
- `static/css/style.css` - Styles globaux
- `static/css/navbar-modern.css` - Navbar
- `static/mentoring/css/*.css` - Styles par page
- `static/accounts/css/profile.css` - Profil

---

## ✅ Points Clés du Système

1. **Un seul dashboard** : `/dashboard/` qui redirige automatiquement
2. **Onboarding automatique** : Middleware gère le flux
3. **Rôles séparés** : Mentor et Étudiant avec fonctionnalités différentes
4. **Profils complets** : Basés sur les données d'onboarding
5. **Sessions de mentorat** : Système complet de réservation et feedback
6. **Design moderne** : Interface utilisateur soignée et responsive

---

## 🚀 Pour Démarrer

1. **Migration** : `python manage.py migrate`
2. **Serveur** : `python manage.py runserver`
3. **Accès** : `http://127.0.0.1:8000/`
4. **Admin** : `http://127.0.0.1:8000/admin/`

---

## 📝 Résumé

**3 Applications Django** :
- **Core** : Pages publiques + Dashboard
- **Accounts** : Utilisateurs + Authentification
- **Mentoring** : Fonctionnalités de mentorat

**Flux Principal** :
Inscription → Sélection rôle → Onboarding → Dashboard → Sessions

**Système Unifié** :
- Un seul point d'entrée pour le dashboard
- Redirection automatique selon le rôle
- Middleware pour gérer l'onboarding

