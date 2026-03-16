# Guide d'Intégration HTMX - Page de Connexion

## Objectif
Améliorer l'expérience utilisateur en mettant à jour uniquement les messages d'erreur sans recharger toute la page lors de la soumission du formulaire de connexion.

## Fichiers Modifiés

### 1. Template Partiel d'Erreur
**Fichier** : [`templates/accounts/partials/error_message.html`](file:///c:/Users/Moussa/Desktop/Mentorxhub/Mentorxhub/templates/accounts/partials/error_message.html)

Template minimal qui affiche uniquement le message d'erreur avec le style existant.

```django
{% if error_message %}
<div class="error-box htmx-error" role="alert" aria-live="polite">
    {{ error_message }}
</div>
{% endif %}
```

### 2. Template Principal de Connexion
**Fichier** : [`templates/accounts/login.html`](file:///c:/Users/Moussa/Desktop/Mentorxhub/Mentorxhub/templates/accounts/login.html)

**Modifications** :
- Ajout du CDN HTMX dans le `<head>`
- Ajout des attributs HTMX au formulaire :
  - `hx-post="{% url 'accounts:login' %}"` : Endpoint de soumission
  - `hx-target="#error-message"` : Cible de mise à jour
  - `hx-swap="innerHTML"` : Mode de remplacement
- Création d'un conteneur `#error-message` pour les erreurs dynamiques
- Ajout d'événements JavaScript pour gérer l'état du bouton pendant les requêtes HTMX

### 3. Vue Django
**Fichier** : [`accounts/views.py`](file:///c:/Users/Moussa/Desktop/Mentorxhub/Mentorxhub/accounts/views.py)

**Modifications de `CustomLoginView`** :
- Détection des requêtes HTMX via `request.headers.get('HX-Request')`
- **En cas d'erreur** :
  - Requête HTMX → Retour du template partiel avec le message
  - Requête normale → Comportement PRG classique (redirect)
- **En cas de succès** :
  - Requête HTMX → Header `HX-Redirect` vers le dashboard
  - Requête normale → Redirect classique

## Comportement

### Avec JavaScript Activé (HTMX)
1. L'utilisateur soumet le formulaire
2. HTMX intercepte la soumission et envoie une requête AJAX
3. Le serveur détecte HTMX et retourne uniquement le fragment HTML de l'erreur
4. HTMX insère ce fragment dans `#error-message`
5. **Pas de rechargement de page**
6. En cas de succès, HTMX redirige vers le dashboard

### Sans JavaScript (Fallback)
Le comportement classique est préservé grâce au pattern Post-Redirect-Get :
1. Soumission POST normale
2. Redirect GET avec messages en session
3. Rechargement complet de la page avec les erreurs

## Avantages

✅ **Fluité** : Pas de rechargement intempestif  
✅ **Rapidité** : Seul le fragment d'erreur est transféré  
✅ **Accessibilité** : Préservation du fonctionnement sans JavaScript  
✅ **Maintenabilité** : Code Django simple et clair  
✅ **Expérience Premium** : Animation smooth des messages

## Message d'Erreur Standard

Le message d'erreur complet utilisé pour les échecs de connexion :

> "Veuillez saisir une adresse e-mail et un mot de passe corrects. Veuillez noter que ces deux champs peuvent être sensibles à la casse."

---

**Date d'implémentation** : 2025-12-01  
**Technologie** : HTMX 1.9.10
