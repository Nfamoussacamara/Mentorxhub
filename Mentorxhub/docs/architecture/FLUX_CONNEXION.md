# 🔐 Flux de Connexion - MentorXHub

## ✅ Système de Redirection Automatique

### 📋 Vue d'Ensemble

Quand un utilisateur se connecte, il est **automatiquement redirigé vers le dashboard approprié** selon son rôle :
- **Mentor** → Dashboard Mentor
- **Étudiant** → Dashboard Étudiant
- **Pas de rôle** → Sélection de rôle → Dashboard

---

## 🔄 Flux Complet

### 1️⃣ Connexion (`/accounts/login/`)

**Vue** : `CustomLoginView` (`accounts/views/auth.py`)

**Comportement** :
- ✅ Authentification réussie → Redirection vers `/dashboard/`
- ✅ Message de bienvenue : "Bienvenue {nom} !"
- ✅ Support HTMX pour les requêtes AJAX

**Code** :
```python
if user is not None:
    login(self.request, user)
    messages.success(self.request, f'Bienvenue {user.get_full_name()} !')
    return redirect('core:dashboard')
```

---

### 2️⃣ Dashboard Principal (`/dashboard/`)

**Vue** : `dashboard()` (`core/views.py`)

**Comportement** :
- ✅ Si `user.role == 'mentor'` → Affiche `dashboard-mentor.html`
- ✅ Si `user.role == 'student'` → Affiche `dashboard-mentee.html`
- ✅ Si `user.role == None` → Redirection vers `/accounts/onboarding/role/`

**Code** :
```python
if user.role == 'mentor':
    return mentor_dashboard(request)
elif user.role == 'student':
    return student_dashboard(request)
else:
    return redirect('accounts:onboarding_role')
```

---

### 3️⃣ Sélection de Rôle (`/accounts/onboarding/role/`)

**Vue** : `RoleSelectionView` (`accounts/views/onboarding/role.py`)

**Comportement** :
- ✅ Si l'utilisateur a déjà un rôle → Redirection vers `/dashboard/`
- ✅ Sinon → Affiche le formulaire de sélection de rôle
- ✅ Après sélection → Redirection vers `/dashboard/`
- ✅ Crée automatiquement le profil (MentorProfile ou StudentProfile)

**Code** :
```python
def form_valid(self, form):
    user.role = form.cleaned_data['role']
    user.save()
    
    if role == 'mentor':
        MentorProfile.objects.get_or_create(user=user)
    elif role == 'student':
        StudentProfile.objects.get_or_create(user=user)
    
    return redirect('core:dashboard')
```

---

### 4️⃣ Middleware d'Onboarding

**Fichier** : `accounts/middleware.py`

**Comportement** :
- ✅ Intercepte les utilisateurs sans rôle
- ✅ Redirige automatiquement vers `/accounts/onboarding/role/`
- ✅ Vérifie l'état de l'onboarding
- ✅ Redirige vers les formulaires d'onboarding si incomplet

**Logique** :
```python
# 1. Vérification du Rôle
if not user.role:
    if path != url_role:
        return redirect(url_role)

# 2. Vérification Onboarding
if not user.onboarding_completed:
    if user.role == 'student':
        target_url = reverse('mentoring:mentee_onboarding')
    elif user.role == 'mentor':
        target_url = reverse('mentoring:mentor_onboarding')
    return redirect(target_url)
```

---

## 🎯 Scénarios de Connexion

### Scénario 1 : Utilisateur avec Rôle Défini

```
1. Utilisateur se connecte → /accounts/login/
2. Authentification réussie
3. Redirection → /dashboard/
4. Dashboard détecte le rôle
5. Affiche le dashboard approprié (mentor ou étudiant)
```

**Résultat** : ✅ Accès direct au dashboard

---

### Scénario 2 : Utilisateur Sans Rôle

```
1. Utilisateur se connecte → /accounts/login/
2. Authentification réussie
3. Redirection → /dashboard/
4. Dashboard détecte l'absence de rôle
5. Redirection → /accounts/onboarding/role/
6. Utilisateur sélectionne un rôle
7. Redirection → /dashboard/
8. Dashboard affiche le dashboard approprié
```

**Résultat** : ✅ Sélection de rôle puis accès au dashboard

---

### Scénario 3 : Utilisateur Sans Rôle (via Middleware)

```
1. Utilisateur se connecte → /accounts/login/
2. Authentification réussie
3. Middleware intercepte (pas de rôle)
4. Redirection → /accounts/onboarding/role/
5. Utilisateur sélectionne un rôle
6. Redirection → /dashboard/
7. Dashboard affiche le dashboard approprié
```

**Résultat** : ✅ Middleware intercepte avant le dashboard

---

### Scénario 4 : Inscription Nouvelle

```
1. Utilisateur s'inscrit → /accounts/signup/
2. Compte créé et connecté automatiquement
3. Redirection → /dashboard/
4. Dashboard détecte l'absence de rôle
5. Redirection → /accounts/onboarding/role/
6. Utilisateur sélectionne un rôle
7. Redirection → /dashboard/
8. Dashboard affiche le dashboard approprié
```

**Résultat** : ✅ Inscription → Sélection de rôle → Dashboard

---

## ⚙️ Configuration

### Settings (`mentorxhub/settings.py`)

```python
# Redirection après connexion
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"
```

### Middleware (`settings.py`)

```python
MIDDLEWARE = [
    # ...
    'accounts.middleware.OnboardingMiddleware',  # Middleware d'onboarding
]
```

---

## 🔒 Sécurité

### Protection des Routes

- ✅ `@login_required` sur toutes les vues dashboard
- ✅ Middleware vérifie l'authentification
- ✅ Redirection automatique si pas de rôle
- ✅ Vérification de l'état d'onboarding

### URLs Exemptées (Middleware)

Les URLs suivantes sont accessibles sans vérification de rôle :
- `/accounts/login/`
- `/accounts/signup/`
- `/accounts/logout/`
- `/accounts/onboarding/role/`
- `/core:home` et pages publiques
- `/mentoring:mentors_list` (liste publique)

---

## 📝 Messages Utilisateur

### Connexion Réussie
```
"Bienvenue {nom} !"
```

### Sélection de Rôle
```
"Rôle {role} sélectionné avec succès !"
```

### Inscription
```
"Bienvenue {nom} ! Votre compte a été créé avec succès."
```

---

## ✅ Points Clés

1. **Redirection Automatique** : Tous les utilisateurs connectés sont redirigés vers `/dashboard/`
2. **Détection de Rôle** : Le dashboard détecte automatiquement le rôle et affiche la vue appropriée
3. **Sélection de Rôle** : Si pas de rôle, redirection automatique vers la sélection
4. **Middleware** : Double sécurité pour intercepter les utilisateurs sans rôle
5. **Onboarding** : Vérification de l'état d'onboarding après sélection du rôle

---

## 🚀 Résultat Final

**Tous les utilisateurs connectés accèdent automatiquement au dashboard approprié :**
- ✅ **Mentor** → Dashboard Mentor avec statistiques et sessions
- ✅ **Étudiant** → Dashboard Étudiant avec sessions et mentors recommandés
- ✅ **Pas de rôle** → Sélection de rôle puis dashboard

**Le système est entièrement automatique et transparent pour l'utilisateur !** 🎉

