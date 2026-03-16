# 🧪 Guide de Test - Phase 1 : Architecture de Base

## ✅ Vérifications Préalables

### 1. Vérifier que l'application est bien installée

```bash
cd Mentorxhub/Mentorxhub
python manage.py check
```

**Résultat attendu** : Aucune erreur

### 2. Vérifier les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

**Résultat attendu** : Pas de nouvelles migrations nécessaires (ou migrations créées/appliquées)

---

## 🚀 Tests Manuels

### Test 1 : Accès au Dashboard (Non Authentifié)

1. Ouvrir le navigateur
2. Aller sur `http://127.0.0.1:8000/dashboard/`
3. **Résultat attendu** : Redirection vers `/accounts/login/?next=/dashboard/`

### Test 2 : Accès au Dashboard (Mentor)

1. Se connecter avec un compte mentor
2. Aller sur `http://127.0.0.1:8000/dashboard/`
3. **Résultat attendu** :
   - ✅ Sidebar visible à gauche avec navigation mentor
   - ✅ Navbar en haut avec avatar utilisateur
   - ✅ Statistiques affichées (Demandes, Sessions, Note, Revenus)
   - ✅ Prochaines sessions listées

### Test 3 : Accès au Dashboard (Étudiant)

1. Se connecter avec un compte étudiant
2. Aller sur `http://127.0.0.1:8000/dashboard/`
3. **Résultat attendu** :
   - ✅ Sidebar visible à gauche avec navigation étudiant
   - ✅ Navbar en haut avec avatar utilisateur
   - ✅ Statistiques affichées (Heures, Sessions, Mentors actifs)
   - ✅ Prochaines sessions listées
   - ✅ Mentors recommandés affichés

### Test 4 : Sidebar - Toggle

1. Cliquer sur le bouton hamburger (mobile) ou toggle (desktop)
2. **Résultat attendu** : Sidebar se réduit/s'étend

### Test 5 : User Menu

1. Cliquer sur l'avatar utilisateur dans la navbar
2. **Résultat attendu** : Menu déroulant avec options (Profil, Paramètres, Déconnexion)

### Test 6 : Theme Toggle

1. Cliquer sur "Mode sombre" dans le menu utilisateur
2. **Résultat attendu** :
   - ✅ Thème passe en dark mode
   - ✅ Préférence sauvegardée (recharger la page pour vérifier)

### Test 7 : Recherche (Ctrl+K)

1. Appuyer sur `Ctrl+K` (ou `Cmd+K` sur Mac)
2. **Résultat attendu** : Barre de recherche s'ouvre

### Test 8 : Responsive (Mobile)

1. Réduire la fenêtre du navigateur à < 1024px
2. **Résultat attendu** :
   - ✅ Sidebar devient un drawer (caché par défaut)
   - ✅ Bouton hamburger visible dans la navbar
   - ✅ Layout s'adapte

---

## 🧪 Tests Automatisés

### Lancer les tests Django

```bash
cd Mentorxhub/Mentorxhub
python manage.py test dashboard.tests --verbosity=2
```

**Tests inclus** :
- ✅ Dashboard redirige les mentors
- ✅ Dashboard redirige les étudiants
- ✅ Dashboard nécessite une authentification
- ✅ Dashboard redirige si pas de rôle

---

## 🔍 Vérifications de Code

### Vérifier les URLs

```bash
python manage.py show_urls | grep dashboard
```

**URLs attendues** :
- `/dashboard/` → `dashboard:dashboard`
- `/dashboard/home/` → `dashboard:home`

### Vérifier les Templates

Les templates suivants doivent exister :
- ✅ `templates/dashboard/base.html`
- ✅ `templates/dashboard/home.html`
- ✅ `templates/dashboard/partials/sidebar.html`
- ✅ `templates/dashboard/partials/navbar.html`
- ✅ `templates/dashboard/fragments/home.html`
- ✅ `templates/dashboard/fragments/mentor_dashboard.html`
- ✅ `templates/dashboard/fragments/student_dashboard.html`

### Vérifier les Fichiers Statiques

Les fichiers suivants doivent exister :
- ✅ `static/dashboard/css/variables.css`
- ✅ `static/dashboard/css/base.css`
- ✅ `static/dashboard/css/home.css`
- ✅ `static/dashboard/js/main.js`

---

## 🐛 Problèmes Courants

### Problème 1 : TemplateNotFound

**Erreur** : `TemplateDoesNotExist: dashboard/base.html`

**Solution** : Vérifier que les templates sont dans `templates/dashboard/` et non `dashboard/templates/`

### Problème 2 : Static files not found

**Erreur** : Les CSS/JS ne se chargent pas

**Solution** :
```bash
python manage.py collectstatic --noinput
```

### Problème 3 : ModuleNotFoundError: No module named 'dashboard'

**Erreur** : L'application n'est pas trouvée

**Solution** : Vérifier que `dashboard` est dans `INSTALLED_APPS` de `settings.py`

### Problème 4 : Sidebar ne s'affiche pas

**Erreur** : Sidebar invisible ou mal positionnée

**Solution** : Vérifier que `base.css` est bien chargé et que les variables CSS sont définies

---

## ✅ Checklist de Validation

- [ ] Serveur démarre sans erreur
- [ ] Dashboard accessible après connexion
- [ ] Sidebar visible et fonctionnelle
- [ ] Navbar visible avec tous les éléments
- [ ] Statistiques affichées correctement
- [ ] Navigation selon le rôle fonctionne
- [ ] Theme toggle fonctionne
- [ ] Responsive sur mobile
- [ ] Tests automatisés passent
- [ ] Aucune erreur dans la console du navigateur

---

## 📝 Notes de Test

**Date** : _______________
**Testeur** : _______________
**Résultat** : ☐ Réussi  ☐ Échec

**Commentaires** :
_________________________________________________
_________________________________________________
_________________________________________________

---

**Une fois tous les tests passés, la Phase 1 est validée ! ✅**

