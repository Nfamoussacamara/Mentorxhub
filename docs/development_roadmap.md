# Roadmap de Développement - MentorXHub

## 📋 Vue d'Ensemble

Ce document présente l'ordre logique de développement après la mise en place de l'authentification (login/signup).

---

## 🗺️ Ordre de Développement Recommandé

### 1️⃣ Dashboard / Page d'Accueil Après Connexion
**Priorité** : ⭐⭐⭐⭐⭐ CRITIQUE

**Pourquoi ?**
C'est la **première chose** que l'utilisateur voit après s'être connecté. C'est la "home base" de l'application.

**Fonctionnalités** :
- **Dashboard Mentor** :
  - Sessions à venir
  - Revenus du mois
  - Nouveaux messages
  - Demandes de réservation en attente
  - Statistiques (nombre d'étudiants, note moyenne)
  
- **Dashboard Étudiant** :
  - Mes prochaines sessions
  - Mentors favoris
  - Progression / Objectifs
  - Sessions passées
  - Recommandations de mentors

**Navigation** :
- Menu vers profil, recherche, messagerie, paramètres
- Widgets cliquables pour actions rapides

**Impact** : Définit toute l'expérience utilisateur et la rétention

---

### 2️⃣ Profils Utilisateur
**Priorité** : ⭐⭐⭐⭐⭐ CRITIQUE

**Pourquoi ?**
Les utilisateurs doivent pouvoir compléter et afficher leurs profils. Sans profils complets, la recherche de mentors n'a pas de sens.

**Fonctionnalités** :

**Profil Mentor** :
- Photo de profil
- Biographie (150-500 mots)
- Domaines d'expertise (tags)
- Tarif horaire
- Expérience professionnelle
- Formations / Certifications
- Langues parlées
- Disponibilités (calendrier)
- Portfolio / Liens (LinkedIn, GitHub, etc.)

**Profil Étudiant** :
- Photo de profil
- Biographie courte
- Objectifs d'apprentissage
- Centres d'intérêt
- Niveau d'étude
- Historique de sessions

**Fonctionnalités techniques** :
- Édition de profil (formulaire ou inline avec HTMX)
- Upload de photo (drag & drop)
- Validation des champs
- Preview en temps réel

**Impact** : Essentiel pour la proposition de valeur de la plateforme

---

### 3️⃣ Recherche et Liste des Mentors
**Priorité** : ⭐⭐⭐⭐⭐ CRITIQUE

**Pourquoi ?**
C'est le **cœur fonctionnel** de MentorXHub. Sans cela, aucune transaction ne peut avoir lieu.

**Fonctionnalités** :

**Page de Recherche** :
- Barre de recherche (nom, compétences)
- Filtres :
  - Domaine d'expertise
  - Fourchette de prix
  - Disponibilité (aujourd'hui, cette semaine, ce mois)
  - Note minimale
  - Langue
- Tri :
  - Pertinence
  - Prix (croissant/décroissant)
  - Note (meilleure en premier)
  - Popularité
  - Nouveaux mentors

**Carte Mentor** :
- Photo
- Nom complet
- Titre / Spécialité
- Tarif horaire
- Note moyenne (étoiles)
- Nombre d'avis
- Badge (Top Mentor, Nouveau, etc.)
- Bouton "Voir profil"
- Icône "Favori"

**Page Détail Mentor** :
- Toutes les infos du profil
- Calendrier de disponibilités
- Bouton "Réserver une session"
- Liste des avis
- Mentors similaires

**Technologies** :
- HTMX pour filtres dynamiques
- Pagination (infinite scroll ou numéros de page)
- Debounce sur la recherche

**Impact** : Core business de la plateforme

---

### 4️⃣ Système de Réservation
**Priorité** : ⭐⭐⭐⭐⭐ CRITIQUE

**Pourquoi ?**
Permet la **conversion** : étudiant → session réservée → revenus.

**Fonctionnalités** :

**Côté Étudiant** :
- Calendrier de disponibilités du mentor
- Sélection de créneaux horaires
- Formulaire de réservation :
  - Date/heure
  - Durée (30min, 1h, 2h)
  - Sujet de la session
  - Message au mentor (optionnel)
  - Mode (visio, présentiel)
- Récapitulatif avec prix total
- Bouton "Confirmer et payer"

**Côté Mentor** :
- Gestion du calendrier :
  - Définir disponibilités récurrentes
  - Bloquer des créneaux
  - Créneaux d'urgence
- Recevoir demandes de réservation
- Accepter/refuser (si validation manuelle activée)

**Email de Confirmation** :
- Email étudiant : Confirmation + lien visio + iCal
- Email mentor : Notification de réservation

**Gestion des Annulations** :
- Politique d'annulation (24h avant, 48h avant, etc.)
- Demande de remboursement
- Notifications

**Impact** : Conversion et monétisation directe

---

### 5️⃣ Paiement
**Priorité** : ⭐⭐⭐⭐ HAUTE

**Pourquoi ?**
Nécessaire pour monétiser et sécuriser les transactions.

**Fonctionnalités** :

**Intégration Stripe (recommandé)** :
- Checkout sécurisé
- Paiement par carte
- Sauvegarde des cartes (optionnel)
- 3D Secure

**Alternative : PayPal**

**Gestion** :
- Commission de la plateforme (ex: 15%)
- Transfert aux mentors (hebdomadaire/mensuel)
- Tableau de bord des revenus
- Historique des transactions
- Factures automatiques (PDF)

**Sécurité** :
- Paiements PCI-DSS compliant
- Webhooks pour confirmer paiements
- Gestion des échecs de paiement

**Impact** : Revenus et crédibilité

---

### 6️⃣ Messagerie
**Priorité** : ⭐⭐⭐⭐ MOYENNE-HAUTE

**Pourquoi ?**
Communication directe entre mentor et étudiant pour préparer les sessions.

**Fonctionnalités** :

**Version Basique (MVP)** :
- Liste des conversations
- Chat 1-to-1
- Envoi de messages texte
- Horodatage
- Indicateur "vu"

**Version Avancée** :
- Temps réel (WebSockets)
- Notifications push
- Partage de fichiers
- Emojis / réactions
- Recherche dans l'historique

**Technologies** :
- HTMX + polling (version simple)
- Django Channels + WebSockets (temps réel)

**Impact** : Rétention et satisfaction utilisateur

---

### 7️⃣ Avis et Notations
**Priorité** : ⭐⭐⭐⭐ MOYENNE-HAUTE

**Pourquoi ?**
Établit la **confiance** et garantit la **qualité** des mentors.

**Fonctionnalités** :

**Laisser un Avis** :
- Formulaire après session terminée
- Note (1 à 5 étoiles)
- Commentaire écrit (150-500 caractères)
- Tags (Pédagogue, Patient, Expert, etc.)
- Anonyme (optionnel)

**Affichage** :
- Note moyenne globale du mentor
- Nombre total d'avis
- Répartition des notes (graphique)
- Liste des avis (tri par date, pertinence)
- Réponse du mentor (optionnel)

**Modération** :
- Vérification des avis
- Signalement d'avis inappropriés
- Suppression si nécessaire

**Impact** : Crédibilité et qualité de la plateforme

---

### 8️⃣ Notifications
**Priorité** : ⭐⭐⭐ MOYENNE

**Pourquoi ?**
Garder les utilisateurs engagés et informés.

**Types de Notifications** :

**In-App (Navbar)** :
- Badge avec nombre de notifications non lues
- Dropdown avec liste
- Marquer comme lu

**Email** :
- Session confirmée
- Session dans 24h (rappel)
- Nouveau message
- Demande d'avis
- Paiement reçu (mentor)

**Push Notifications** (optionnel, mobile) :
- Nouveau message
- Session imminente

**Paramètres** :
- Permettre à l'utilisateur de choisir :
  - Types de notifications
  - Fréquence
  - Canaux (email, in-app, push)

**Impact** : Engagement et rétention

---

### 9️⃣ Admin & Modération
**Priorité** : ⭐⭐⭐ MOYENNE-BASSE

**Pourquoi ?**
Gérer le contenu, les utilisateurs et les litiges.

**Fonctionnalités** :

**Dashboard Admin Django** :
- Gestion des utilisateurs (activer/désactiver)
- Modération des avis
- Gestion des signalements
- Statistiques globales
- Export de données

**Analytics** :
- Nombre d'inscriptions (par jour/semaine/mois)
- Taux de conversion
- Revenus
- Mentors actifs / inactifs
- Sessions réalisées

**Gestion des Litiges** :
- Interface pour traiter les remboursements
- Historique des actions admin
- Logs de sécurité

**Impact** : Gestion efficace de la plateforme

---

## 🎯 Approche MVP (Minimum Viable Product)

### Phase 1 : Flow de Base (2-3 semaines)
**Objectif** : Permettre le parcours complet étudiant

1. Dashboard basique (liste de sessions)
2. Profil mentor (formulaire simple, sans upload photo)
3. Liste des mentors (grille simple, sans filtres)
4. Réservation simple (formulaire + email de confirmation)

**Résultat** : Un étudiant peut trouver un mentor et réserver une session

---

### Phase 2 : Amélioration UX (1-2 semaines)
**Objectif** : Rendre l'expérience fluide et moderne

5. HTMX sur recherche (filtres dynamiques)
6. Calendrier interactif (FullCalendar.js)
7. Upload de photos de profil
8. Dashboard enrichi (widgets, stats)

**Résultat** : Interface professionnelle et agréable

---

### Phase 3 : Monétisation (1 semaine)
**Objectif** : Activer les paiements

9. Intégration Stripe
10. Page de paiement sécurisée
11. Calculation automatique de la commission
12. Génération de factures

**Résultat** : Plateforme monétisable

---

### Phase 4 : Engagement (1-2 semaines)
**Objectif** : Fidéliser les utilisateurs

13. Messagerie basique
14. Système d'avis et notations
15. Notifications email
16. Favoris

**Résultat** : Utilisateurs engagés et qui reviennent

---

### Phase 5 : Optimisation (Continu)
**Objectif** : Améliorer performances et features

17. Temps réel (WebSockets pour chat)
18. Notifications push
19. Analytics avancées
20. SEO et marketing

**Résultat** : Plateforme mature et scalable

---

## 🛠️ Stack Technologique Recommandée

**Backend** :
- Django 5.x
- Django REST Framework (API si besoin)
- Celery (tâches asynchrones : emails, notifications)
- Redis (cache, sessions)

**Frontend** :
- HTMX (interactions dynamiques)
- Alpine.js (JS léger pour interactions complexes)
- TailwindCSS ou CSS custom (déjà en place)

**Paiements** :
- Stripe

**Email** :
- Django Email (SMTP)
- SendGrid / Mailgun (production)

**Temps Réel** :
- Django Channels + WebSockets (chat)

**Infrastructure** :
- PostgreSQL (base de données)
- AWS S3 / Cloudinary (stockage médias)
- Heroku / DigitalOcean / AWS (déploiement)

---

## 📊 Métriques de Succès

**Phase MVP** :
- [ ] 10 mentors inscrits avec profil complet
- [ ] 50 étudiants inscrits
- [ ] 20 sessions réservées
- [ ] Taux de conversion : 5% (étudiants → réservation)

**Phase Croissance** :
- [ ] 100+ mentors
- [ ] 1000+ étudiants
- [ ] 200+ sessions/mois
- [ ] Taux de rétention : 40% (retour dans les 30 jours)

**Phase Maturité** :
- [ ] 500+ mentors
- [ ] 10 000+ étudiants
- [ ] 1000+ sessions/mois
- [ ] Note moyenne plateforme : 4.5+/5

---

**Dernière mise à jour** : 2025-12-01  
**Prochaine étape** : À définir avec l'équipe
