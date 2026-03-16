# Logique de la Sidebar - MentorXHub

## 📋 Vue d'ensemble

La sidebar du dashboard utilise un système d'activation dynamique pour indiquer la page actuelle à l'utilisateur.

---

## 🎯 Système d'activation des liens

### Principe de base

Chaque lien de navigation a une classe conditionnelle `active` qui s'applique selon la page visitée :

```html
<a href="URL" class="nav-item {% if CONDITION %}active{% endif %}">
```

### Détection de la page active

#### 1. **Vue d'ensemble**
```html
{% if request.resolver_match.url_name == 'dashboard' or request.resolver_match.url_name == 'home' %}active{% endif %}
```
- **Condition** : Le nom de l'URL Django est `dashboard` OU `home`
- **Activation** : Page d'accueil du dashboard

#### 2. **Sessions**
```html
{% if request.resolver_match.url_name == 'analytics' %}active{% endif %}
```
- **Condition** : Le nom de l'URL Django est `analytics`
- **Activation** : Page d'analyse des sessions
- **Route** : `/dashboard/analytics/`

#### 3. **Mentors**
```html
{% if 'mentors' in request.path %}active{% endif %}
```
- **Condition** : Le mot "mentors" est présent dans le chemin de l'URL
- **Activation** : N'importe quelle page contenant `/mentors/`
- **Exemples** :
  - `/mentoring/mentors/` ✅
  - `/mentoring/mentors/123/` ✅
  - `/dashboard/profile/` ❌

#### 4. **Messagerie**
```html
{% if request.resolver_match.url_name|startswith:'message' %}active{% endif %}
```
- **Condition** : Le nom de l'URL commence par "message"
- **Activation** : Toutes les pages de messagerie
- **Exemples de noms d'URL** :
  - `messages_list` ✅
  - `messages_detail` ✅
  - `message_send` ✅

#### 5. **Cours**
```html
{% if request.resolver_match.url_name|startswith:'course' %}active{% endif %}
```
- **Condition** : Le nom de l'URL commence par "course"
- **Activation** : Toutes les pages de cours

---

## 🎨 Styles CSS appliqués

### État normal (.nav-item)
```css
.nav-item {
    background-color: transparent;
    color: var(--gray-700);
}
```

### État hover (.nav-item:hover)
```css
.nav-item:hover {
    background-color: rgba(255, 255, 255, 0.5);
    color: var(--gray-900);
}
```

### État actif (.nav-item.active)
```css
.nav-item.active {
    background-color: var(--white);
    color: var(--gray-900);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

---

## 📐 Logique de redimensionnement

### Desktop (> 1024px)

#### Largeurs supportées
- **Minimum** : 70px (mode icônes uniquement)
- **Maximum** : 400px
- **Par défaut** : 260px

#### Affichage progressif (70px - 150px)
```javascript
if (newWidth < 150) {
    const opacity = (newWidth - 70) / 80; // Calcul de 0 à 1
    // Opacité progressive des labels
}
```

**Formule d'opacité** :
- À 70px → opacity = 0 (invisible)
- À 110px → opacity = 0.5 (semi-visible)
- À 150px → opacity = 1 (complètement visible)

#### Sauvegarde de l'état
```javascript
localStorage.setItem('sidebarWidth', sidebar.style.width);
localStorage.setItem('sidebarCollapsed', isCollapsed);
```

### Mobile/Tablette (≤ 1024px)

#### Comportements
- **Largeur fixe** : 280px (mobile) / 300px (tablette)
- **Mode overlay** : La sidebar se superpose au contenu
- **Swipe** : Glisser vers la gauche pour fermer
- **Resizer désactivé** : Pas de redimensionnement manuel

#### Fermeture automatique
```javascript
// Clic en dehors de la sidebar
if (!sidebar.contains(e.target)) {
    sidebar.classList.remove('open');
}

// Swipe vers la gauche
if (touchStartX - touchEndX > 50) {
    sidebar.classList.remove('open');
}
```

---

## 🔄 Préservation de l'état

### Problème résolu
Lors de la navigation entre pages, la sidebar pouvait perdre sa largeur personnalisée.

### Solution
```javascript
function preserveSidebarState() {
    // Vérifier toutes les 500ms que la largeur est correcte
    const savedWidth = localStorage.getItem('sidebarWidth');
    if (sidebar.style.width !== savedWidth + 'px') {
        sidebar.style.width = savedWidth + 'px';
    }
}

setInterval(preserveSidebarState, 500);
```

### Exclusion mobile
```javascript
// Ne pas appliquer sur mobile/tablette
if (window.innerWidth <= 1024) return;
```

---

## 🎭 Modes d'affichage

### Mode Normal (> 150px)
- Labels visibles
- Icônes alignées à gauche
- Badge de notifications visible

### Mode Réduit (70px - 150px)
- Labels en fade progressif
- Icônes centrées graduellement
- Badge en fade

### Mode Collapsed (70px fixe)
```css
.dashboard-sidebar.collapsed .nav-label {
    opacity: 0;
    width: 0;
    overflow: hidden;
}

.dashboard-sidebar.collapsed .nav-item {
    justify-content: center;
}
```

---

## 🔍 Variables Django utilisées

### request.resolver_match.url_name
- **Type** : String
- **Valeur** : Nom de l'URL défini dans `urls.py`
- **Exemple** : `'dashboard'`, `'analytics'`, `'messages_list'`

### request.path
- **Type** : String
- **Valeur** : Chemin complet de l'URL
- **Exemple** : `'/dashboard/mentoring/mentors/'`

### Filtres Django
- `|startswith:'text'` : Vérifie si commence par "text"
- `in` : Vérifie si contient

---

## 🛠️ Points techniques clés

### 1. Pourquoi différentes méthodes de détection ?

**URL name** (`url_name == 'analytics'`)
- ✅ Plus précis
- ✅ Indépendant de la structure d'URL
- ❌ Ne fonctionne que pour une page exacte

**Path matching** (`'mentors' in request.path`)
- ✅ Fonctionne pour plusieurs pages
- ✅ Capture toutes les sous-pages
- ❌ Peut avoir des faux positifs

**Startswith** (`url_name|startswith:'message'`)
- ✅ Équilibre entre précision et couverture
- ✅ Suit les conventions de nommage Django
- ✅ Couvre toute une section

### 2. Ordre de priorité CSS
```
.nav-item.active > .nav-item:hover > .nav-item
```

### 3. Performance
- **localStorage** : Lecture/écriture asynchrone
- **setInterval(500ms)** : Vérification légère toutes les demi-secondes
- **Transitions CSS** : Hardware-accelerated (GPU)

---

## 📱 Breakpoints responsive

```css
/* Desktop */
@media (min-width: 1025px) { /* Resize actif */ }

/* Tablette */
@media (min-width: 768px) and (max-width: 1024px) { /* 300px fixe */ }

/* Mobile */
@media (max-width: 767px) { /* 280px fixe */ }
```

---

## 🚀 Améliorations futures possibles

1. **Animation d'activation** : Transition smooth lors du changement de page
2. **Breadcrumb sync** : Synchroniser avec le fil d'Ariane
3. **Keyboard navigation** : Support des flèches clavier
4. **Submenu** : Support de sous-menus déroulants
5. **Favoris** : Permettre d'épingler des pages fréquentes

---

**Date de création** : 16 décembre 2025  
**Version** : 1.0  
**Auteur** : GitHub Copilot
