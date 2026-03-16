# ✅ Correction des URLs Dashboard

## Problème Résolu

Toutes les références à `'core:dashboard'` ont été remplacées par `'dashboard:dashboard'` car le dashboard a été déplacé vers l'application dédiée `dashboard`.

## Fichiers Modifiés

### Vues Python
- ✅ `accounts/views/auth.py` - 3 occurrences corrigées
- ✅ `accounts/views/onboarding/role.py` - 2 occurrences corrigées
- ✅ `mentoring/views/main.py` - 1 occurrence corrigée
- ✅ `mentoring/views/onboarding/mentor.py` - 1 occurrence corrigée
- ✅ `mentoring/views/onboarding/mentee.py` - 5 occurrences corrigées

### Templates
- ✅ `accounts/templates/accounts/profile.html` - 1 occurrence corrigée
- ✅ `templates/base.html` - 1 occurrence corrigée

### Tests
- ✅ `accounts/tests/test_middleware.py` - 1 occurrence corrigée

## Changements Effectués

### Avant
```python
return redirect('core:dashboard')
reverse('core:dashboard')
reverse_lazy('core:dashboard')
```

### Après
```python
return redirect('dashboard:dashboard')
reverse('dashboard:dashboard')
reverse_lazy('dashboard:dashboard')
```

### Dans les Templates
```django
<!-- Avant -->
<a href="{% url 'core:dashboard' %}">

<!-- Après -->
<a href="{% url 'dashboard:dashboard' %}">
```

## Résultat

Maintenant, après l'inscription ou la connexion, les utilisateurs sont correctement redirigés vers `/dashboard/` qui utilise le namespace `dashboard:dashboard`.

L'erreur `NoReverseMatch: Reverse for 'dashboard' not found` est résolue ! ✅

