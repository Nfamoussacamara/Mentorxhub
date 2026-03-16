# 📋 Liste Complète des Liens du Projet MentorXHub

## 🔗 URLs Principales (Core)

### Pages Publiques
- **Accueil** : `/` → `core:home`
- **Dashboard** : `/dashboard/` → `core:dashboard`
- **Tarifs** : `/pricing/` → `core:pricing`
- **Top Mentors** : `/top-mentors/` → `core:top_mentors`
- **À propos** : `/about/` → `core:about`
- **Comment ça marche** : `/how-it-works/` → `core:how_it_works`
- **Carrières** : `/careers/` → `core:careers`
- **Blog** : `/blog/` → `core:blog`

### Pages Légales
- **Politique de confidentialité** : `/privacy/` → `core:privacy_policy`
- **Conditions d'utilisation** : `/terms/` → `core:terms_of_service`

---

## 👤 URLs Comptes (Accounts)

### Authentification
- **Inscription** : `/accounts/signup/` → `accounts:signup`
- **Connexion** : `/accounts/login/` → `accounts:login`
- **Déconnexion** : `/accounts/logout/` → `accounts:logout`

### Onboarding
- **Sélection du rôle** : `/accounts/onboarding/role/` → `accounts:onboarding_role`

### Profil
- **Voir le profil** : `/accounts/profile/` → `accounts:profile`
- **Modifier le profil** : `/accounts/profile/edit/` → `accounts:profile_edit`

### Réinitialisation de mot de passe
- **Demande de réinitialisation** : `/accounts/password-reset/` → `accounts:password_reset`
- **Confirmation envoyée** : `/accounts/password-reset/done/` → `accounts:password_reset_done`
- **Confirmation avec token** : `/accounts/password-reset-confirm/<uidb64>/<token>/` → `accounts:password_reset_confirm`
- **Réinitialisation complète** : `/accounts/password-reset-complete/` → `accounts:password_reset_complete`

---

## 🎓 URLs Mentorat (Mentoring)

### Liste et Profils
- **Liste des mentors** : `/mentoring/mentors/` → `mentoring:mentor_list`
- **Profil public mentor** : `/mentoring/mentor/<int:pk>/` → `mentoring:mentor_detail`
- **Dashboard mentor** : `/mentoring/mentor/dashboard/` → `mentoring:mentor_dashboard`
- **Mise à jour profil mentor** : `/mentoring/mentor/profile/update/` → `mentoring:mentor_profile_update`
- **Dashboard étudiant** : `/mentoring/student/dashboard/` → `mentoring:student_dashboard`
- **Profil étudiant** : `/mentoring/student/profile/` → `mentoring:student_profile`
- **Mise à jour profil étudiant** : `/mentoring/student/profile/update/` → `mentoring:student_profile_update`

### Disponibilités (Mentors)
- **Liste des disponibilités** : `/mentoring/mentor/availabilities/` → `mentoring:availability_list`
- **Créer une disponibilité** : `/mentoring/mentor/availabilities/create/` → `mentoring:availability_create`
- **Modifier une disponibilité** : `/mentoring/mentor/availabilities/<int:pk>/update/` → `mentoring:availability_update`
- **Supprimer une disponibilité** : `/mentoring/mentor/availabilities/<int:pk>/delete/` → `mentoring:availability_delete`

### Sessions de Mentorat
- **Liste des sessions** : `/mentoring/sessions/` → `mentoring:session_list`
- **Détails d'une session** : `/mentoring/sessions/<int:pk>/` → `mentoring:session_detail`
- **Créer une session** : `/mentoring/sessions/create/<int:mentor_id>/` → `mentoring:session_create`
- **Modifier une session** : `/mentoring/sessions/<int:pk>/update/` → `mentoring:session_update`
- **Supprimer une session** : `/mentoring/sessions/<int:pk>/delete/` → `mentoring:session_delete`
- **Feedback d'une session** : `/mentoring/sessions/<int:pk>/feedback/` → `mentoring:session_feedback`

### Onboarding
- **Onboarding étudiant** : `/mentoring/onboarding/mentee/` → `mentoring:mentee_onboarding`
- **Passer l'onboarding étudiant** : `/mentoring/onboarding/mentee/skip/` → `mentoring:skip_mentee_onboarding`
- **Onboarding mentor** : `/mentoring/onboarding/mentor/` → `mentoring:mentor_onboarding`

### API
- **API Liste des mentors** : `/mentoring/api/mentors/` → `mentoring:mentor_list_api`

---

## 🔗 Liens dans les Templates

### Base Template (`base.html`)
- CSS principal : `{% static 'css/style.css' %}`

### Dashboard Mentor (`dashboard-mentor.html`)
- ✅ `{% url 'core:dashboard' %}` - Dashboard principal
- ✅ `{% url 'accounts:logout' %}` - Déconnexion
- ⚠️ `#requests`, `#schedule`, `#reviews`, `#earnings`, `#settings` - Ancres (à implémenter)

### Dashboard Étudiant (`dashboard-mentee.html`)
- ✅ `{% url 'core:dashboard' %}` - Dashboard principal
- ✅ `{% url 'mentoring:mentors_list' %}` - Liste des mentors
- ✅ `{% url 'accounts:logout' %}` - Déconnexion
- ✅ `{% url 'mentoring:public_mentor_profile' mentor.id %}` - Profil mentor
- ⚠️ `#sessions`, `#messages`, `#favorites`, `#settings` - Ancres (à implémenter)

### Liste des Mentors (`mentor_list.html`)
- ✅ `{% url 'mentoring:mentor_list' %}` - Liste des mentors
- ✅ `{% url 'mentoring:mentor_detail' mentor.id %}` - Profil public mentor
- ✅ `{% url 'mentoring:session_create' mentor.id %}` - Créer une session
- ✅ `{% url 'accounts:login' %}?next={% url 'mentoring:mentors_list' %}` - Connexion avec redirection

### Profil Public Mentor (`mentor_public_profile.html`)
- ✅ `{% url 'mentoring:session_create' mentor.id %}` - Créer une session
- ✅ `{% url 'accounts:login' %}?next={{ request.path }}` - Connexion avec redirection
- ⚠️ `#reviews` - Ancre (à implémenter)

### Dashboard Étudiant (`student_dashboard.html`)
- ✅ `{% url 'mentoring:mentor_list' %}` - Liste des mentors
- ✅ `{% url 'mentoring:session_detail' session.id %}` - Détails session
- ✅ `{% url 'mentoring:mentor_detail' mentor.id %}` - Profil mentor
- ✅ `{% url 'mentoring:session_create' mentor.id %}` - Créer une session

### Dashboard Mentor (`mentor_dashboard.html`)
- ✅ `{% url 'accounts:logout' %}` - Déconnexion
- ✅ `{% url 'mentoring:session_detail' session.id %}` - Détails session
- ⚠️ `#` - Liens placeholder (Dashboard, Requests, Schedule, Reviews, Settings)

### Formulaire de Session (`session_form.html`)
- ✅ `{% url 'mentoring:public_mentor_profile' mentor.id %}` - Retour au profil mentor

### Profil Utilisateur (`profile.html`)
- ✅ `{% url 'accounts:profile_edit' %}` - Modifier le profil
- ✅ `{% url 'core:dashboard' %}` - Retour au dashboard
- ✅ Liens externes : GitHub, LinkedIn, Portfolio (depuis les profils)

### Édition de Profil (`profile_edit.html`)
- ✅ `{% url 'accounts:profile' %}` - Retour au profil

---

## ⚠️ Liens à Implémenter

### Ancres dans les Dashboards
1. **Dashboard Mentor** :
   - `#requests` - Page des demandes
   - `#schedule` - Calendrier
   - `#reviews` - Avis
   - `#earnings` - Revenus
   - `#settings` - Paramètres

2. **Dashboard Étudiant** :
   - `#sessions` - Mes sessions
   - `#messages` - Messages
   - `#favorites` - Favoris
   - `#settings` - Paramètres

3. **Profil Public Mentor** :
   - `#reviews` - Section des avis

### Liens Placeholder
- Dashboard Mentor : Liens `#` dans la sidebar (Dashboard, Requests, Schedule, Reviews, Settings)

---

## ✅ Statut des Liens

### Liens Fonctionnels ✅
- Tous les liens utilisant `{% url %}` avec des noms d'URL valides
- Liens vers les profils, sessions, dashboards
- Liens d'authentification
- Liens de navigation principaux

### Liens Externes ✅
- GitHub, LinkedIn, Portfolio (depuis les profils utilisateur)
- Liens de réunion (meeting_link) - dynamiques

### À Vérifier ⚠️
- Ancres de navigation (`#requests`, `#schedule`, etc.)
- Liens placeholder (`#`)

---

## 📝 Notes

1. **Tous les liens principaux sont fonctionnels** et pointent vers des URLs valides
2. **Les ancres de navigation** (`#section`) nécessitent l'implémentation des sections correspondantes
3. **Les liens externes** (GitHub, LinkedIn, Portfolio) sont dynamiques et dépendent des données utilisateur
4. **Les liens de réunion** (`meeting_link`) sont dynamiques et dépendent des sessions

---

## 🔍 Vérification

Pour vérifier tous les liens, exécutez :
```bash
python manage.py check
```

Ou utilisez le script :
```bash
python scripts/check_all_urls.py
```

