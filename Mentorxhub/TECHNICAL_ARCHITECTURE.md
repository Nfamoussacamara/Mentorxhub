# 🏗️ Architecture Technique MentorXHub

Ce document détaille l'architecture technique du projet, les choix technologiques et la structure des applications.

## 📌 Vue d'ensemble

Le projet est une application Django monolithique modulaire, divisée en 4 applications principales :

| Application | Responsabilité | Cible |
| :--- | :--- | :--- |
| **`accounts`** | Authentification (Email/OAuth), Gestion utilisateurs (`CustomUser`), Onboarding. | Tous |
| **`mentoring`** | Profils (Mentor/Mentee), Gestion des sessions, Recherche de mentors. | Tous |
| **`dashboard`** | Interface principale post-login. Hub centralisé pour toutes les fonctionnalités. | Utilisateurs connectés |
| **`core`** | Pages publiques, Marketing, Landing page, Pages légales. | Visiteurs |

---

## 🚀 Architecture Dashboard (SPA-like)

Le Dashboard (`/dashboard/`) utilise une architecture **"HTML-over-the-wire"** pour offrir une expérience utilisateur fluide type Single Page Application (SPA), sans la complexité d'un framework JS lourd (React/Vue).

### 🛠️ Stack Technique Dashboard

*   **HTMX** : Moteur principal de l'interactivité. Remplace la navigation standard par des requêtes AJAX qui remplacent dynamiquement des portions du DOM.
*   **Django Templates** : Rendu côté serveur. Les vues renvoient des fragments HTML lors des requêtes HTMX.
*   **CSS Moderne** : Variables CSS, Dark Mode natif, composants modulaires.
*   **Chart.js** : (Implémentation prévue) Visualisation de données via endpoints JSON.

### 📂 Structure HTMX

HTMX est intégré via `hx-boost` sur le conteneur principal, interceptant les clics sur les liens pour charger le contenu via AJAX.

**Fichiers Clés HTMX :**
*   `templates/dashboard/base.html` : Configuration racine (`hx-boost="true"`, `hx-target="this"`).
*   `templates/dashboard/fragments/*.html` : Fragments de template renvoyés pour les requêtes AJAX (widgets, listes, formulaires).
*   `static/dashboard/js/htmx-init.js` : Configuration globale et gestion des événements HTMX.
*   `accounts/templates/accounts/login.html` : Formulaire de connexion optimisé HTMX.

---

## 🔐 Authentification & Utilisateurs (`accounts`)

*   **Modèle** : `CustomUser` (utilise `email` comme identifiant, pas de `username`).
*   **Flux** :
    1.  Inscription/Connexion (Email ou Google OAuth via `django-allauth`).
    2.  **Middleware d'Onboarding** : Vérifie si l'utilisateur a choisi son rôle.
    3.  **Redirection** : Force la sélection du rôle (Mentor ou Étudiant) si manquant.

---

## 🎓 Mentorat (`mentoring`)

*   **Profils** : Extension du user via `MentorProfile` (OneToOne) et `StudentProfile`.
*   **Workflows** :
    *   **Mentor** : Inscription -> Validation requise (Status: Pending -> Approved).
    *   **Student** : Inscription directe.
*   **Sessions** : Modèle `MentoringSession` pour le cycle de vie d'une rencontre (Planifiée -> En cours -> Terminée/Annulée).

---

## 🎨 Frontend Tooling

Le projet privilégie une approche **No-Build** (ou Low-Build) pour le frontend.
*   **Pas de Node.js/Webpack** requis pour le développement standard.
*   **CSS** : Vanilla CSS avec variables pour la thématisation.
*   **Icônes** : FontAwesome 6 (chargé via CDN/Static).
