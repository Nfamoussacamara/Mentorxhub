# 📁 Structure Complète du Projet MentorXHub

## Vue d'ensemble

**MentorXHub** est une plateforme de mentorat développée avec Django 6.0, permettant la mise en relation entre mentors et étudiants (mentorés). Le projet suit une architecture modulaire avec séparation claire des responsabilités.

---

## 🗂️ Structure Racine du Projet

```
Mentorxhub/
├── docs/                          # Documentation générale du projet
├── Mentorxhub/                    # Dossier principal de l'application Django
├── mon_env/                       # Environnement virtuel Python
└── manage.py                      # Script de gestion Django
```

---

## 📂 Dossier `docs/` (Documentation Générale)

**Rôle** : Contient toute la documentation du projet, guides, rapports et mockups.

### Fichiers principaux :
- `dashboard_student_mockup.md` : Mockup du dashboard étudiant
- `development_roadmap.md` : Roadmap de développement
- `error_messages_french.md` : Messages d'erreur en français
- `google_oauth_implementation.md` : Guide d'implémentation OAuth Google
- `google_oauth_role_handling.md` : Gestion des rôles avec OAuth
- `htmx_integration_guide.md` : Guide d'intégration HTMX
- `htmx_strategy.md` : Stratégie de migration vers HTMX
- `login_page_report.md` : Rapport sur la page de connexion
- `signals_documentation.md` : Documentation des signaux Django
- `signup_google_mockup.md` : Mockup d'inscription avec Google
- `verification_inscription.md` : Processus de vérification d'inscription

---

## 📂 Dossier `Mentorxhub/` (Application Django Principale)

C'est le cœur de l'application Django. Il contient toutes les applications, configurations, templates, fichiers statiques et médias.

### Structure principale :

```
Mentorxhub/
├── accounts/              # Application d'authentification et gestion des utilisateurs
├── core/                  # Application pour les pages publiques
├── dashboard/             # Application du tableau de bord
├── mentoring/             # Application de gestion du mentorat
├── mentorxhub/            # Configuration principale Django
├── templates/             # Templates HTML globaux
├── static/                # Fichiers statiques (CSS, JS, images)
├── staticfiles/           # Fichiers statiques collectés (production)
├── media/                 # Fichiers médias uploadés par les utilisateurs
├── scripts/               # Scripts utilitaires Python
├── docs/                  # Documentation technique interne
├── db.sqlite3             # Base de données SQLite (développement)
├── manage.py              # Script de gestion Django
└── requirements.txt       # Dépendances Python du projet
```

---

## 🔐 Application `accounts/` (Authentification et Utilisateurs)

**Rôle** : Gère l'authentification, l'inscription, la connexion, les profils utilisateurs et l'onboarding.

### Structure :

```
accounts/
├── __init__.py
├── admin.py                    # Configuration admin Django
├── apps.py                     # Configuration de l'application
├── models.py                   # Modèle CustomUser (sans username, email uniquement)
├── forms.py                    # Formulaires d'inscription, connexion, profil
├── urls.py                     # Routes URL de l'application
├── signals.py                  # Signaux Django (création de profils)
├── middleware.py               # Middleware d'onboarding personnalisé
├── adapters.py                 # Adapters pour django-allauth
│
├── services/                   # Services métier
│   ├── __init__.py
│   └── role_transition.py      # Service de transition de rôle (mentor ↔ étudiant)
│
├── views/                      # Vues organisées par module
│   ├── __init__.py
│   ├── auth.py                 # Vues d'authentification (login, signup, logout)
│   ├── profile.py              # Vues de profil utilisateur
│   └── onboarding/
│       └── role_selection.py   # Vue de sélection de rôle
│
├── templates/accounts/          # Templates HTML
│   ├── login.html
│   ├── signup.html
│   ├── role_selection.htmlr
│   ├── profile.html
│   └── password_reset*.html
│
├── static/accounts/            # Fichiers statiques spécifiques
│   ├── css/                    # Styles CSS
│   ├── js/                     # Scripts JavaScript
│   └── img/                    # Images
│
├── migrations/                 # Migrations de base de données
│   └── 0001_initial.py à 0006_*.py
│
└── tests/                      # Tests unitaires
    ├── test_middleware.py
    └── test_role_transition.py
```

### Modèles principaux :
- **CustomUser** : Modèle utilisateur personnalisé (email comme identifiant unique, pas de username)
  - Champs : `email`, `first_name`, `last_name`, `role` (mentor/student), `bio`, `avatar`, `banner`, `onboarding_completed`, etc.

### Fonctionnalités clés :
- Authentification par email/mot de passe
- Authentification OAuth Google (via django-allauth)
- Sélection de rôle lors de l'onboarding
- Transition de rôle (mentor ↔ étudiant)
- Middleware d'onboarding pour rediriger les utilisateurs non-onboardés
- Gestion des profils utilisateurs

---

## 🌐 Application `core/` (Pages Publiques)

**Rôle** : Gère les pages publiques du site (accueil, à propos, tarifs, etc.) et les fonctionnalités communes.

### Structure :

```
core/
├── __init__.py
├── admin.py
├── apps.py
├── models.py                   # Modèles communs (si nécessaire)
├── urls.py                     # Routes des pages publiques
├── views.py                    # Vues des pages publiques
├── tests.py                    # Tests
│
├── templates/core/             # Templates des pages publiques
│   ├── home.html
│   ├── pricing.html
│   ├── about.html
│   ├── how_it_works.html
│   ├── careers.html
│   ├── blog.html
│   ├── privacy_policy.html
│   └── terms_of_service.html
│
├── static/core/                # Fichiers statiques
│   ├── css/                    # Styles CSS
│   └── js/                     # Scripts JavaScript
│
├── templatetags/               # Tags de template personnalisés
│   ├── __init__.py
│   └── custom_filters.py       # Filtres personnalisés (ex: message_time)
│
└── migrations/                 # Migrations (si modèles)
```

### Pages publiques :
- `/` : Page d'accueil
- `/pricing/` : Tarifs
- `/top-mentors/` : Top mentors
- `/about/` : À propos
- `/how-it-works/` : Comment ça marche
- `/careers/` : Carrières
- `/blog/` : Blog
- `/privacy/` : Politique de confidentialité
- `/terms/` : Conditions d'utilisation

### Filtres personnalisés :
- `message_time` : Formate l'heure des messages (ex: "Il y a 5 minutes")

---

## 📊 Application `dashboard/` (Tableau de Bord)

**Rôle** : Application principale du tableau de bord pour mentors et étudiants. Gère toutes les fonctionnalités du dashboard.

### Structure :

```
dashboard/
├── __init__.py
├── admin.py                    # Configuration admin
├── apps.py
├── models.py                   # Modèles du dashboard (Conversation, Message, Course, etc.)
├── urls.py                     # Routes URL du dashboard
├── forms.py                    # Formulaires du dashboard
├── managers.py                  # Managers personnalisés pour les modèles
├── mixins.py                   # Mixins réutilisables (RoleRequiredMixin)
├── decorators.py               # Décorateurs personnalisés
├── utils.py                    # Utilitaires
├── signals.py                  # Signaux Django
│
├── views/                      # Vues organisées par module
│   ├── __init__.py
│   ├── dashboard.py            # Vues principales du dashboard
│   ├── profile.py              # Vues de profil dans le dashboard
│   ├── messages.py             # Vues de messagerie
│   ├── notifications.py        # Vues de notifications
│   ├── analytics.py            # Vues d'analytics
│   ├── sessions.py             # Vues de sessions
│   ├── courses.py              # Vues de cours
│   ├── payments.py             # Vues de paiements
│   ├── support.py              # Vues de support
│   └── settings.py             # Vues de paramètres
│
├── templates/dashboard/        # Templates du dashboard
│   ├── base.html               # Template de base du dashboard
│   ├── home.html               # Page d'accueil du dashboard
│   │
│   ├── partials/               # Partials réutilisables
│   │   ├── sidebar.html        # Barre latérale de navigation
│   │   └── navbar.html         # Barre de navigation supérieure
│   │
│   ├── fragments/              # Fragments HTMX réutilisables
│   │   ├── overview_dashboard.html      # Vue d'ensemble du dashboard
│   │   ├── messages_list_panel.html    # Liste des conversations
│   │   ├── messages_chat_panel.html     # Panneau de chat
│   │   ├── notifications_list.html     # Liste des notifications
│   │   ├── analytics.html              # Analytics
│   │   ├── courses_list.html           # Liste des cours
│   │   ├── course_create.html          # Création de cours
│   │   ├── course_detail.html          # Détail d'un cours
│   │   ├── lesson_detail.html          # Détail d'une leçon
│   │   ├── payments_list.html          # Liste des paiements
│   │   ├── payment_create.html          # Création de paiement
│   │   ├── payment_detail.html          # Détail d'un paiement
│   │   ├── sessions_calendar.html       # Calendrier des sessions
│   │   ├── session_detail.html          # Détail d'une session
│   │   ├── support_tickets_list.html    # Liste des tickets
│   │   ├── support_ticket_create.html   # Création de ticket
│   │   ├── support_ticket_detail.html   # Détail d'un ticket
│   │   ├── support_faq.html             # FAQ
│   │   ├── profile_view.html            # Vue du profil
│   │   ├── settings.html                # Paramètres
│   │   ├── settings_general.html        # Paramètres généraux
│   │   ├── settings_security.html       # Paramètres de sécurité
│   │   ├── settings_notifications.html  # Paramètres de notifications
│   │   ├── mentor_dashboard.html       # Dashboard spécifique mentor
│   │   └── student_dashboard.html       # Dashboard spécifique étudiant
│   │
│   ├── messages/               # Templates de messagerie
│   │   ├── list.html           # Liste des conversations
│   │   └── conversation.html  # Conversation détaillée
│   │
│   ├── notifications/          # Templates de notifications
│   │   └── list.html
│   │
│   ├── analytics/              # Templates d'analytics
│   │   └── view.html
│   │
│   ├── courses/                # Templates de cours
│   │   ├── list.html
│   │   ├── create.html
│   │   ├── detail.html
│   │   ├── edit.html
│   │   ├── lesson_create.html
│   │   └── lesson_detail.html
│   │
│   ├── payments/               # Templates de paiements
│   │   ├── list.html
│   │   ├── create.html
│   │   └── detail.html
│   │
│   ├── sessions/               # Templates de sessions
│   │   ├── calendar.html
│   │   └── detail.html
│   │
│   ├── support/                # Templates de support
│   │   ├── tickets_list.html
│   │   ├── ticket_create.html
│   │   ├── ticket_detail.html
│   │   └── faq.html
│   │
│   ├── profile/                # Templates de profil
│   │   ├── view.html
│   │   └── edit.html
│   │
│   └── settings/               # Templates de paramètres
│       └── view.html
│
├── static/dashboard/           # Fichiers statiques du dashboard
│   ├── css/                    # Styles CSS
│   │   ├── variables.css      # Variables CSS (couleurs, espacements)
│   │   ├── base.css            # Styles de base (layout, sidebar, navbar)
│   │   ├── components.css      # Composants réutilisables
│   │   ├── modules.css         # Styles des modules
│   │   ├── dashboard-overview.css  # Styles de la vue d'ensemble
│   │   ├── messages.css        # Styles de la messagerie
│   │   ├── analytics.css       # Styles des analytics
│   │   ├── premium-cards.css   # Styles des cartes premium
│   │   └── premium-components.css  # Composants premium
│   │
│   └── js/                     # Scripts JavaScript
│       ├── main.js             # Script principal (sidebar, navbar, thème)
│       ├── utils.js            # Utilitaires JavaScript
│       ├── htmx-init.js        # Initialisation HTMX
│       ├── dashboard-overview.js  # Scripts de la vue d'ensemble (Chart.js)
│       ├── messages.js         # Scripts de messagerie
│       ├── notifications.js   # Scripts de notifications
│       ├── analytics.js        # Scripts d'analytics
│       ├── courses.js          # Scripts de cours
│       ├── payments.js         # Scripts de paiements
│       ├── sessions.js         # Scripts de sessions
│       ├── support.js          # Scripts de support
│       ├── settings.js         # Scripts de paramètres
│       └── core/               # Scripts core réutilisables
│           ├── state_manager.js    # Gestionnaire d'état
│           ├── api_client.js       # Client API
│           └── router.js           # Routeur (obsolète, remplacé par HTMX)
│
├── migrations/                 # Migrations de base de données
│   └── 0001_initial.py
│
└── tests/                      # Tests unitaires
    ├── test_models.py
    ├── test_views.py
    ├── test_forms.py
    ├── test_managers.py
    ├── test_mixins.py
    └── test_utils.py
```

### Modèles principaux :
- **UserProfile** : Profil utilisateur étendu
- **Conversation** : Conversation entre utilisateurs
- **Message** : Messages dans une conversation
- **Notification** : Notifications utilisateur
- **Course** : Cours créés par les mentors
- **Lesson** : Leçons dans un cours
- **Payment** : Paiements
- **SupportTicket** : Tickets de support
- **Analytics** : Données d'analytics

### Fonctionnalités clés :
- Dashboard personnalisé selon le rôle (mentor/étudiant)
- Messagerie en temps réel (avec HTMX polling)
- Système de notifications
- Analytics et statistiques
- Gestion de cours et leçons
- Calendrier de sessions
- Gestion des paiements
- Système de support (tickets, FAQ)
- Paramètres utilisateur (général, sécurité, notifications, thème)
- Mode sombre/clair
- Intégration HTMX pour interactions dynamiques

---

## 👥 Application `mentoring/` (Gestion du Mentorat)

**Rôle** : Gère la mise en relation entre mentors et étudiants, les profils publics, les disponibilités et les sessions de mentorat.

### Structure :

```
mentoring/
├── __init__.py
├── admin.py                    # Configuration admin
├── apps.py
├── models.py                   # Modèles (MentorProfile, StudentProfile, MentoringSession, etc.)
├── urls.py                     # Routes URL
├── forms.py                    # Formulaires
├── api_views.py                # Vues API (pour AJAX/JSON)
│
├── views/                      # Vues organisées par module
│   ├── __init__.py
│   ├── mentor_views.py         # Vues liées aux mentors
│   ├── student_views.py        # Vues liées aux étudiants
│   ├── session_views.py         # Vues de sessions
│   ├── availability_views.py   # Vues de disponibilités
│   └── onboarding_views.py     # Vues d'onboarding
│
├── templates/mentoring/         # Templates
│   ├── mentor_list.html
│   ├── mentor_profile.html
│   ├── student_profile.html
│   ├── session_list.html
│   ├── session_detail.html
│   ├── session_create.html
│   ├── availability_list.html
│   ├── mentor_onboarding.html
│   └── mentee_onboarding.html
│
├── static/mentoring/            # Fichiers statiques
│   ├── css/                    # Styles CSS
│   └── js/                     # Scripts JavaScript
│
├── migrations/                 # Migrations
│   └── 0001_initial.py à 0004_*.py
│
└── tests/                      # Tests
    ├── test_models.py
    └── test_views.py
```

### Modèles principaux :
- **MentorProfile** : Profil détaillé d'un mentor
  - Champs : `expertise`, `years_of_experience`, `hourly_rate`, `languages`, `certifications`, `rating`, `status` (pending/approved/rejected), etc.
- **StudentProfile** : Profil détaillé d'un étudiant
  - Champs : `level`, `learning_goals`, `interests`, `preferred_languages`, etc.
- **Availability** : Disponibilités d'un mentor
- **MentoringSession** : Session de mentorat entre un mentor et un étudiant
- **SessionFeedback** : Feedback sur une session

### Fonctionnalités clés :
- Liste publique des mentors
- Profils publics de mentors et étudiants
- Gestion des disponibilités des mentors
- Création et gestion de sessions de mentorat
- Système de feedback
- Onboarding séparé pour mentors et mentorés

---

## ⚙️ Dossier `mentorxhub/` (Configuration Django)

**Rôle** : Contient les fichiers de configuration principaux de Django.

### Structure :

```
mentorxhub/
├── __init__.py
├── settings.py                 # Configuration Django (apps, middleware, base de données, etc.)
├── urls.py                     # URLs racine du projet
├── wsgi.py                     # Configuration WSGI (production)
├── asgi.py                     # Configuration ASGI (WebSockets, async)
└── scripts/                    # Scripts de configuration
    └── setup.md                # Documentation de setup
```

### Fichiers clés :

#### `settings.py` :
- **INSTALLED_APPS** : Applications installées (core, accounts, mentoring, dashboard, allauth, etc.)
- **MIDDLEWARE** : Middleware Django (sécurité, sessions, auth, onboarding)
- **DATABASES** : Configuration SQLite (développement)
- **AUTH_USER_MODEL** : `accounts.CustomUser`
- **STATIC_URL**, **MEDIA_URL** : Configuration des fichiers statiques et médias
- **AUTHENTICATION_BACKENDS** : Backends d'authentification (Django + allauth)
- **ACCOUNT_ADAPTER**, **SOCIALACCOUNT_ADAPTER** : Adapters personnalisés
- **SOCIALACCOUNT_PROVIDERS** : Configuration OAuth Google

#### `urls.py` :
- Routes principales du projet
- Inclusion des URLs des applications (`core`, `accounts`, `mentoring`, `dashboard`, `allauth`)

---

## 📄 Dossier `templates/` (Templates HTML Globaux)

**Rôle** : Templates HTML partagés entre les applications.

### Structure :

```
templates/
├── base.html                   # Template de base global
├── home.html                   # Page d'accueil (obsolète ?)
├── dashboard-mentee.html       # Template dashboard mentoré (obsolète ?)
├── dashboard-mentor.html       # Template dashboard mentor (obsolète ?)
│
├── accounts/                    # Templates accounts (doublons ?)
│   └── ...
│
├── core/                       # Templates core (pages publiques)
│   └── ...
│
└── dashboard/                  # Templates dashboard (voir section dashboard/)
    └── ...
```

**Note** : Certains templates peuvent être des doublons ou obsolètes. Vérifier la cohérence.

---

## 🎨 Dossier `static/` (Fichiers Statiques)

**Rôle** : Fichiers statiques (CSS, JavaScript, images) utilisés par l'application.

### Structure :

```
static/
├── css/                        # CSS globaux
│   ├── main.css
│   └── ...
│
├── js/                         # JavaScript globaux
│   ├── main.js
│   └── ...
│
├── img/                        # Images globales
│   ├── logo.png
│   └── ...
│
├── dashboard/                  # Fichiers statiques du dashboard
│   ├── css/                    # (voir section dashboard/)
│   └── js/                     # (voir section dashboard/)
│
├── accounts/                   # Fichiers statiques accounts
│   └── ...
│
├── core/                       # Fichiers statiques core
│   └── ...
│
└── mentoring/                  # Fichiers statiques mentoring
    └── ...
```

---

## 📁 Dossier `staticfiles/` (Fichiers Statiques Collectés)

**Rôle** : Fichiers statiques collectés par `python manage.py collectstatic` pour la production.

**Note** : Ce dossier est généré automatiquement et ne doit pas être modifié manuellement. Il contient une copie de tous les fichiers statiques de toutes les applications.

---

## 🖼️ Dossier `media/` (Fichiers Médias)

**Rôle** : Fichiers uploadés par les utilisateurs (avatars, images de profil, bannières, etc.).

### Structure :

```
media/
├── profile_pics/               # Photos de profil
│   └── IMG-20250607-WA00061.jpg
│
├── mentor/                     # Fichiers spécifiques mentors
│   └── ...
│
└── Mentee/                     # Fichiers spécifiques mentorés
    └── ...
```

---

## 🛠️ Dossier `scripts/` (Scripts Utilitaires)

**Rôle** : Scripts Python utilitaires pour la gestion du projet.

### Structure :

```
scripts/
├── README.md                   # Documentation des scripts
├── create_admin.py             # Créer un superutilisateur
├── create_test_user.py         # Créer un utilisateur de test
├── approve_user.py              # Approuver un utilisateur
├── check_database.py            # Vérifier la base de données
├── check_all_urls.py            # Vérifier toutes les URLs
└── test_dashboard.py            # Tester le dashboard
```

---

## 📚 Dossier `Mentorxhub/docs/` (Documentation Technique Interne)

**Rôle** : Documentation technique interne au projet Django.

### Structure :

```
Mentorxhub/docs/
├── architecture/               # Documentation d'architecture
│   └── ...
│
├── archive/                    # Documentation archivée
│   ├── dashboard/             # Anciens docs dashboard
│   ├── fixes/                 # Anciens correctifs
│   ├── phases/                # Documentation par phases
│   └── tests/                 # Anciens tests
│
├── guides/                     # Guides techniques
│   └── ...
│
├── HTMX_MIGRATION.md          # Documentation de migration HTMX
├── HTMX_VERIFICATION.md       # Vérification de la migration HTMX
├── CORRECTIONS_TEMPLATE.md    # Template de corrections
├── REFACTORISATION_TEMPLATE_VERS_VUE.md  # Refactorisation templates
├── DOCUMENTATION_INDEX.md     # Index de la documentation
├── ETAT_FINAL_PROJET.md       # État final du projet
├── LIENS_PROJET.md            # Liens utiles du projet
├── RESUME_CAHIERS_CHARGES.md  # Résumé des cahiers des charges
├── RESUME_FINAL_TOUTES_PHASES.md  # Résumé de toutes les phases
├── RESUME_LIENS.md            # Résumé des liens
├── TECHNICAL_ARCHITECTURE.md  # Architecture technique
└── PLAN_REORGANISATION.md     # Plan de réorganisation
```

---

## 🗄️ Fichiers Racine Importants

### `manage.py`
Script de gestion Django. Utilisé pour :
- `python manage.py runserver` : Lancer le serveur de développement
- `python manage.py migrate` : Appliquer les migrations
- `python manage.py collectstatic` : Collecter les fichiers statiques
- `python manage.py createsuperuser` : Créer un superutilisateur
- etc.

### `requirements.txt`
Liste des dépendances Python du projet :
- Django 6.0
- django-allauth 65.13.1 (OAuth)
- Pillow 12.0.0 (traitement d'images)
- django-crispy-forms (formulaires Bootstrap)
- crispy-bootstrap5
- etc.

### `db.sqlite3`
Base de données SQLite (développement). Contient toutes les tables et données.

### `CHANGELOG.md`
Journal des modifications du projet.

### `readme.md`
README principal du projet.

### `run_tests.py`
Script pour exécuter les tests.

---

## 🔄 Flux de Données et Interactions

### 1. Authentification
```
Utilisateur → accounts/views/auth.py → accounts/models.py (CustomUser)
           → accounts/adapters.py (allauth)
           → Redirection vers dashboard/
```

### 2. Dashboard
```
Utilisateur → dashboard/views/dashboard.py
           → dashboard/templates/dashboard/home.html
           → dashboard/templates/dashboard/fragments/overview_dashboard.html
           → HTMX pour rafraîchissement automatique
```

### 3. Messagerie
```
Utilisateur → dashboard/views/messages.py
           → dashboard/models.py (Conversation, Message)
           → HTMX polling pour nouveaux messages
           → dashboard/templates/dashboard/fragments/messages_chat_panel.html
```

### 4. Sessions de Mentorat
```
Utilisateur → mentoring/views/session_views.py
           → mentoring/models.py (MentoringSession)
           → dashboard/views/sessions.py (calendrier)
```

---

## 🎯 Technologies et Bibliothèques Utilisées

### Backend
- **Django 6.0** : Framework web Python
- **django-allauth** : Authentification OAuth (Google)
- **Pillow** : Traitement d'images
- **django-crispy-forms** : Formulaires Bootstrap

### Frontend
- **HTMX** : Interactions dynamiques sans JavaScript complexe
- **Chart.js** : Graphiques et visualisations
- **Font Awesome** : Icônes
- **Bootstrap 5** : Framework CSS (via crispy-forms)

### Base de données
- **SQLite** : Base de données de développement

---

## 📝 Notes Importantes

1. **Architecture modulaire** : Chaque application Django a sa propre responsabilité
2. **HTMX** : Migration récente d'AJAX vers HTMX pour simplifier le code JavaScript
3. **Templates fragments** : Utilisation de fragments HTMX pour le chargement dynamique
4. **Mode sombre** : Support du mode sombre/clair dans le dashboard
5. **Rôles** : Gestion de deux rôles principaux (mentor/étudiant) avec possibilité de transition
6. **Onboarding** : Processus d'onboarding séparé pour mentors et mentorés
7. **Messagerie temps réel** : Utilisation de HTMX polling pour les nouveaux messages

---

## 🚀 Commandes Utiles

```bash
# Activer l'environnement virtuel
mon_env\Scripts\activate  # Windows
source mon_env/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver

# Collecter les fichiers statiques
python manage.py collectstatic

# Exécuter les tests
python manage.py test
python run_tests.py
```

---

## 📞 Points de Contact et Ressources

- **Documentation Django** : https://docs.djangoproject.com/
- **Documentation HTMX** : https://htmx.org/
- **Documentation django-allauth** : https://docs.allauth.org/

---

*Documentation générée le : 2025-12-11*
*Version du projet : 1.0*
*Dernière mise à jour : Migration HTMX complétée*

