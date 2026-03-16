# Stratégie HTMX pour MentorXHub

## ✅ Déjà Implémenté

- **Page de connexion** : Validation du formulaire sans rechargement

## 🎯 Candidats Prioritaires pour HTMX

### 1. Formulaire d'Inscription (Haute Priorité)
**Fichier** : `templates/accounts/signup.html`

**Améliorations possibles** :
- Validation en temps réel des champs (email déjà utilisé, force du mot de passe)
- Soumission sans rechargement
- Messages d'erreur inline par champ

**Bénéfices** :
- Meilleure expérience utilisateur lors de l'inscription
- Feedback immédiat sur la disponibilité de l'email
- Réduction du taux d'abandon

**Exemple d'implémentation** :
```html
<!-- Vérification de l'email en temps réel -->
<input type="email" name="email" 
       hx-post="/api/check-email/"
       hx-trigger="blur"
       hx-target="#email-status"
       hx-indicator="#email-spinner">
<span id="email-status"></span>
```

---

### 2. Recherche et Filtrage de Mentors (Haute Priorité)
**Fonctionnalité** : Liste des mentors avec filtres

**Améliorations possibles** :
- Filtres dynamiques (domaine, disponibilité, tarif)
- Recherche instantanée par nom/compétences
- Pagination sans rechargement
- Tri (par note, prix, expérience)

**Bénéfices** :
- Navigation fluide entre les résultats
- Combinaison de filtres instantanée
- Expérience type "application native"

**Exemple d'implémentation** :
```html
<!-- Filtres de recherche -->
<select name="domain" 
        hx-get="/mentors/list/"
        hx-target="#mentor-list"
        hx-trigger="change"
        hx-include="[name='availability'], [name='price']">
    <option value="">Tous les domaines</option>
    <option value="tech">Technologie</option>
    <!-- ... -->
</select>

<div id="mentor-list">
    <!-- Liste des mentors mise à jour dynamiquement -->
</div>
```

---

### 3. Gestion des Sessions / Réservations (Moyenne Priorité)
**Fonctionnalité** : Calendrier et réservation de sessions

**Améliorations possibles** :
- Affichage du calendrier sans rechargement
- Réservation d'un créneau en modal HTMX
- Annulation/modification de session
- Mise à jour automatique de la disponibilité

**Bénéfices** :
- Réservation rapide et fluide
- Éviter les doubles réservations
- Interface réactive

**Exemple d'implémentation** :
```html
<!-- Clic sur un créneau disponible -->
<button hx-get="/sessions/book/{{ slot.id }}/"
        hx-target="#booking-modal"
        hx-swap="innerHTML"
        class="time-slot available">
    14:00 - 15:00
</button>

<div id="booking-modal">
    <!-- Modal de réservation chargé dynamiquement -->
</div>
```

---

### 4. Profils Utilisateur (Moyenne Priorité)
**Fonctionnalité** : Édition de profil mentor/étudiant

**Améliorations possibles** :
- Édition inline (cliquer pour modifier)
- Sauvegarde automatique
- Upload de photo de profil sans rechargement
- Ajout/suppression de compétences

**Bénéfices** :
- Édition fluide et moderne
- Pas de perte de contexte
- Feedback visuel immédiat

**Exemple d'implémentation** :
```html
<!-- Édition inline de la bio -->
<div hx-get="/profile/edit/bio/"
     hx-trigger="click"
     hx-target="this"
     hx-swap="outerHTML">
    <p>{{ user.bio }}</p>
    <button>✏️ Modifier</button>
</div>
```

---

### 5. Système de Notation / Avis (Moyenne Priorité)
**Fonctionnalité** : Laisser un avis sur un mentor

**Améliorations possibles** :
- Soumission d'avis sans rechargement
- Système de "like" instantané
- Affichage des nouveaux avis en temps réel

**Bénéfices** :
- Encourager plus d'avis
- Interaction sociale fluide
- Mise à jour de la note moyenne instantanée

---

### 6. Messagerie / Chat (Basse Priorité mais Impactant)
**Fonctionnalité** : Conversation entre mentor et étudiant

**Améliorations possibles** :
- Polling automatique (nouveaux messages)
- Envoi de message sans rechargement
- Notifications en temps réel

**Bénéfices** :
- Expérience de chat moderne
- Réactivité perçue accrue

**Note** : Pour du vrai temps réel, considérer WebSockets + HTMX

---

### 7. Tableaux de Bord (Basse Priorité)
**Fonctionnalité** : Dashboard mentor/étudiant

**Améliorations possibles** :
- Rafraîchissement automatique des statistiques
- Widgets chargeables indépendamment
- Actions rapides (accepter/refuser session)

**Bénéfices** :
- Dashboard vivant
- Performances (chargement partiel)

---

## 🛠️ Bonnes Pratiques HTMX pour MentorXHub

### 1. Structure des Templates
Créer un dossier `partials/` dans chaque app :
```
templates/
├── mentoring/
│   ├── mentor_list.html (page complète)
│   └── partials/
│       ├── mentor_card.html (fragment)
│       ├── session_form.html (fragment)
│       └── filters.html (fragment)
```

### 2. Vues Django
Détecter HTMX systématiquement :
```python
def mentor_list(request):
    mentors = Mentor.objects.all()
    
    # Détection HTMX
    if request.headers.get('HX-Request'):
        template = 'mentoring/partials/mentor_cards.html'
    else:
        template = 'mentoring/mentor_list.html'
    
    return render(request, template, {'mentors': mentors})
```

### 3. Messages d'Erreur / Succès
Utiliser des templates partiels réutilisables :
```django
<!-- partials/message.html -->
{% if message %}
<div class="alert alert-{{ message.type }}">
    {{ message.text }}
</div>
{% endif %}
```

### 4. Indicateurs de Chargement
Ajouter des spinners pour les actions longues :
```html
<button hx-post="/action/"
        hx-indicator="#spinner">
    Enregistrer
</button>
<span id="spinner" class="htmx-indicator">⏳ Chargement...</span>
```

---

## 📋 Plan d'Implémentation Recommandé

### Phase 1 : Formulaires (Semaine 1)
- ✅ Login (déjà fait)
- [ ] Signup
- [ ] Édition de profil

### Phase 2 : Listes et Recherche (Semaine 2)
- [ ] Recherche de mentors
- [ ] Filtres dynamiques
- [ ] Pagination

### Phase 3 : Interactions (Semaine 3)
- [ ] Réservation de sessions
- [ ] Système d'avis
- [ ] Actions rapides (like, favoris)

### Phase 4 : Temps Réel (Optionnel)
- [ ] Messagerie
- [ ] Notifications
- [ ] Dashboard live

---

## 🔗 Ressources

- [Documentation HTMX](https://htmx.org/docs/)
- [Exemples HTMX](https://htmx.org/examples/)
- [HTMX + Django Guide](https://htmx.org/essays/django/)

---

**Dernière mise à jour** : 2025-12-01  
**Prochaine étape** : Implémenter HTMX sur le formulaire d'inscription
