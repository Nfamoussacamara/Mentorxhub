# 🔄 Fonctionnement du Système MentorXHub

## 📦 Les 3 Applications Django

### 1. **CORE** - Pages Publiques & Dashboard
```
📍 Emplacement : core/
🎯 Rôle : Interface publique et point d'entrée principal

Fonctions :
- Page d'accueil (/)
- Dashboard principal (/dashboard/) → Redirige selon le rôle
- Pages publiques (tarifs, à propos, blog, etc.)
- Pages légales (politique, conditions)
```

### 2. **ACCOUNTS** - Utilisateurs & Authentification
```
📍 Emplacement : accounts/
🎯 Rôle : Gestion des comptes utilisateurs

Fonctions :
- Modèle utilisateur personnalisé (CustomUser)
- Connexion / Inscription / Déconnexion
- Profils utilisateur (affichage et édition)
- Sélection de rôle (mentor ou étudiant)
- OAuth Google
- Middleware d'onboarding (redirection automatique)
```

### 3. **MENTORING** - Fonctionnalités de Mentorat
```
📍 Emplacement : mentoring/
🎯 Rôle : Cœur métier de la plateforme

Fonctions :
- Profils mentor et étudiant
- Liste et recherche de mentors
- Disponibilités des mentors
- Sessions de mentorat
- Onboarding mentor/étudiant
- Feedback et évaluations
```

---

## 🔄 Flux Principal du Système

### **Étape 1 : Inscription / Connexion**
```
Utilisateur → /accounts/signup/ ou /accounts/login/
    ↓
Authentification réussie
    ↓
Redirection automatique → /dashboard/
```

### **Étape 2 : Vérification du Rôle (Middleware)**
```
Middleware OnboardingMiddleware intercepte
    ↓
Vérifie : user.role existe ?
    ↓
NON → Redirection → /accounts/onboarding/role/
OUI → Continue vers dashboard
```

### **Étape 3 : Sélection du Rôle (si nécessaire)**
```
/accounts/onboarding/role/
    ↓
Utilisateur choisit : Mentor ou Étudiant
    ↓
Création automatique du profil :
- Mentor → MentorProfile
- Étudiant → StudentProfile
    ↓
Redirection → /dashboard/
```

### **Étape 4 : Dashboard Principal**
```
/dashboard/ → core/views.py → dashboard()
    ↓
Vérification du rôle :
    ↓
┌─────────────────┬─────────────────┐
│   Si MENTOR     │  Si ÉTUDIANT     │
├─────────────────┼─────────────────┤
│ mentor_dashboard│student_dashboard │
│     ()          │      ()          │
│        ↓        │        ↓         │
│ dashboard-      │ dashboard-       │
│ mentor.html     │ mentee.html      │
│                 │                  │
│ Statistiques :  │ Statistiques :   │
│ - Demandes      │ - Heures         │
│ - Sessions      │ - Sessions       │
│ - Note          │ - Mentors actifs │
│ - Revenus       │                  │
│                 │ + Mentors        │
│ Sessions avec   │ recommandés      │
│ étudiants       │                  │
└─────────────────┴─────────────────┘
```

---

## 🗄️ Modèles de Données

### **CustomUser** (accounts/models.py)
```
Utilisateur de base :
├── email (unique, utilisé pour connexion)
├── first_name, last_name
├── role (mentor/student/null)
├── bio
├── profile_picture
├── banner_image
└── onboarding_completed
```

### **MentorProfile** (mentoring/models.py)
```
Profil Mentor (lié à CustomUser) :
├── expertise
├── years_of_experience
├── hourly_rate
├── languages
├── rating
├── total_sessions
├── status (pending/approved/rejected)
└── is_available
```

### **StudentProfile** (mentoring/models.py)
```
Profil Étudiant (lié à CustomUser) :
├── level
├── learning_goals
├── interests
├── preferred_languages
├── github_profile
└── total_sessions
```

### **MentoringSession** (mentoring/models.py)
```
Session de Mentorat :
├── mentor (ForeignKey → MentorProfile)
├── student (ForeignKey → StudentProfile)
├── title, description
├── date, start_time, end_time
├── status (scheduled/in_progress/completed/cancelled)
├── meeting_link
└── rating, feedback
```

---

## 🔐 Système d'Authentification

### **Deux Méthodes de Connexion**

1. **Email + Mot de passe**
   - Formulaire classique
   - Vue : `CustomLoginView`

2. **Google OAuth**
   - Connexion via Google
   - Géré par django-allauth
   - Création automatique du compte

### **Redirection Après Connexion**
```
Connexion réussie
    ↓
LOGIN_REDIRECT_URL = "/dashboard/"
    ↓
Redirection → /dashboard/
    ↓
Middleware vérifie le rôle
    ↓
Si pas de rôle → /accounts/onboarding/role/
Si rôle existe → Dashboard approprié
```

---

## 🎯 Dashboard Unifié

### **Un Seul Point d'Entrée**
```
/dashboard/ → core:dashboard
```

### **Redirection Automatique**
```
dashboard() vérifie user.role :
    ↓
if role == 'mentor':
    → mentor_dashboard() → dashboard-mentor.html
    
elif role == 'student':
    → student_dashboard() → dashboard-mentee.html
    
else:
    → redirect('accounts:onboarding_role')
```

### **Avantages**
- ✅ Un seul lien à retenir : `/dashboard/`
- ✅ Redirection automatique selon le rôle
- ✅ Gestion automatique des utilisateurs sans rôle
- ✅ Pas de confusion entre différents dashboards

---

## 🔧 Middleware d'Onboarding

### **OnboardingMiddleware** (accounts/middleware.py)

**Fonction** : Intercepte toutes les requêtes et vérifie l'état de l'utilisateur

**Logique** :
```
1. Vérifie si l'utilisateur est authentifié
    ↓
2. Vérifie si l'utilisateur a un rôle
   NON → Redirection → /accounts/onboarding/role/
   OUI → Continue
    ↓
3. Vérifie si l'onboarding est complété
   NON → Redirection → /mentoring/onboarding/mentor/ ou /mentee/
   OUI → Accès normal
```

**URLs Exemptées** (pas de redirection) :
- Pages publiques (home, pricing, about, etc.)
- Pages d'authentification (login, signup, logout)
- Page de sélection de rôle
- Pages d'onboarding
- Admin Django

---

## 📊 Flux Complet d'un Nouvel Utilisateur

```
1. INSCRIPTION
   /accounts/signup/
   ↓
2. COMPTE CRÉÉ
   CustomUser créé (sans rôle)
   ↓
3. CONNEXION AUTOMATIQUE
   Utilisateur connecté
   ↓
4. REDIRECTION
   → /dashboard/
   ↓
5. MIDDLEWARE INTERCEPTE
   Détecte : pas de rôle
   ↓
6. REDIRECTION
   → /accounts/onboarding/role/
   ↓
7. SÉLECTION DU RÔLE
   Utilisateur choisit : Mentor ou Étudiant
   ↓
8. CRÉATION DU PROFIL
   MentorProfile ou StudentProfile créé
   ↓
9. REDIRECTION
   → /dashboard/
   ↓
10. MIDDLEWARE INTERCEPTE
    Détecte : rôle existe mais onboarding incomplet
    ↓
11. REDIRECTION
    → /mentoring/onboarding/mentor/ ou /mentee/
    ↓
12. FORMULAIRE D'ONBOARDING
    Utilisateur remplit les informations
    ↓
13. ONBOARDING COMPLÉTÉ
    onboarding_completed = True
    ↓
14. REDIRECTION
    → /dashboard/
    ↓
15. DASHBOARD AFFICHÉ
    Dashboard mentor ou étudiant selon le rôle
```

---

## 🎨 Système de Templates

### **Hiérarchie**
```
base.html (template de base)
    ├── Navbar moderne
    ├── Footer
    └── Blocs :
        - {% block content %}
        - {% block extra_css %}
        - {% block extra_js %}
```

### **Templates par Application**

**Core** :
- `home.html` - Page d'accueil
- `dashboard-mentor.html` - Dashboard mentor
- `dashboard-mentee.html` - Dashboard étudiant
- `core/pricing.html` - Tarifs
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

---

## 🔗 Système de Routage

### **URLs Racine** (`mentorxhub/urls.py`)
```
/ → core.urls (pages publiques)
/accounts/ → accounts.urls (authentification)
/mentoring/ → mentoring.urls (mentorat)
/admin/ → Django admin
```

### **Namespaces**
- `core:` - Pages publiques et dashboard
- `accounts:` - Authentification et profils
- `mentoring:` - Fonctionnalités de mentorat

### **Exemple d'URL**
```
{% url 'mentoring:public_mentor_profile' mentor.id %}
→ Résout en : /mentoring/mentor/1/
```

---

## ✅ Points Clés à Retenir

1. **3 Applications** : Core, Accounts, Mentoring
2. **Un seul dashboard** : `/dashboard/` qui redirige automatiquement
3. **Middleware intelligent** : Gère l'onboarding automatiquement
4. **Rôles séparés** : Mentor et Étudiant avec fonctionnalités différentes
5. **Onboarding en 2 étapes** : Sélection de rôle → Formulaire d'onboarding
6. **Profils liés** : CustomUser → MentorProfile ou StudentProfile

---

## 🚀 Pour Tester le Système

1. **Créer un compte** : `http://127.0.0.1:8000/accounts/signup/`
2. **Se connecter** : `http://127.0.0.1:8000/accounts/login/`
3. **Dashboard** : `http://127.0.0.1:8000/dashboard/`
4. **Liste mentors** : `http://127.0.0.1:8000/mentoring/mentors/`
5. **Profil** : `http://127.0.0.1:8000/accounts/profile/`

---

## 📝 Résumé Visuel

```
┌─────────────────────────────────────────┐
│         UTILISATEUR                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    ACCOUNTS (Authentification)           │
│  - Inscription / Connexion              │
│  - Sélection de rôle                    │
│  - Profil utilisateur                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    MIDDLEWARE (OnboardingMiddleware)    │
│  - Vérifie le rôle                       │
│  - Vérifie l'onboarding                 │
│  - Redirige automatiquement             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    CORE (Dashboard Principal)            │
│  - /dashboard/                           │
│  - Redirige selon le rôle               │
│  - Affiche dashboard mentor ou étudiant  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    MENTORING (Fonctionnalités)           │
│  - Liste mentors                         │
│  - Sessions de mentorat                 │
│  - Disponibilités                       │
│  - Feedback                             │
└─────────────────────────────────────────┘
```

---

**Le système est conçu pour être simple, automatique et intuitif !** 🎯

