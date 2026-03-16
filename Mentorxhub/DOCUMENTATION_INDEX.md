# 📚 Index de la Documentation - MentorXHub

Ce document sert d'index central pour toute la documentation du projet.

---

## 📖 Documentation Principale

### 1. Journal des Modifications
**Fichier** : [`CHANGELOG.md`](CHANGELOG.md)  
**Description** : Journal de toutes les modifications, corrections et nouvelles fonctionnalités  
**Mise à jour** : À chaque modification du projet

### 2. Rapport de Tests
**Fichier** : [`TEST_REPORT.md`](TEST_REPORT.md)  
**Description** : Rapport complet des tests effectués, packages installés et vérifications  
**Mise à jour** : Après chaque série de tests

### 3. Recommandations d'Amélioration
**Fichier** : [`RECOMMANDATIONS_AMELIORATION.md`](RECOMMANDATIONS_AMELIORATION.md)  
**Description** : Recommandations détaillées pour améliorer le projet avec priorités et exemples de code  
**Mise à jour** : Après analyse du projet

### 4. Stratégie de Priorisation
**Fichier** : [`PRIORISATION_STRATEGIE.md`](PRIORISATION_STRATEGIE.md)  
**Description** : Explication de la stratégie de développement (Monétisation vs Engagement)  
**Mise à jour** : Quand la stratégie change

### 5. Architecture Technique
**Fichier** : [`TECHNICAL_ARCHITECTURE.md`](TECHNICAL_ARCHITECTURE.md)
**Description** : Vue d'ensemble technique, structure des apps et tooling dashboard (HTMX, SPA-less)
**Mise à jour** : Evolutions architecturales majeures

---

## 📁 Documentation dans `/docs`

### Authentification et OAuth
- [`google_oauth_implementation.md`](../docs/google_oauth_implementation.md) - Implémentation Google OAuth
- [`google_oauth_role_handling.md`](../docs/google_oauth_role_handling.md) - Gestion des rôles avec OAuth
- [`login_page_report.md`](../docs/login_page_report.md) - Rapport sur la page de connexion
- [`signup_user_journey.md`](../docs/signup_user_journey.md) - Parcours d'inscription utilisateur
- [`refactorisation_auth_separation.md`](../docs/refactorisation_auth_separation.md) - **NOUVEAU** - Séparation HTML/CSS/JS pour Login et Signup

### Onboarding
- [`verification_inscription.md`](../docs/verification_inscription.md) - Vérification du système d'inscription
- [`signals_documentation.md`](../docs/signals_documentation.md) - Documentation des signals Django

### Interface et UX
- [`htmx_integration_guide.md`](../docs/htmx_integration_guide.md) - Guide d'intégration HTMX
- [`htmx_strategy.md`](../docs/htmx_strategy.md) - Stratégie HTMX
- [`dashboard_student_mockup.md`](../docs/dashboard_student_mockup.md) - Mockup dashboard étudiant
- [`signup_google_mockup.md`](../docs/signup_google_mockup.md) - Mockup inscription Google

### Patterns et Bonnes Pratiques
- [`prg_pattern_reference.md`](../docs/prg_pattern_reference.md) - Pattern Post-Redirect-Get
- [`error_messages_french.md`](../docs/error_messages_french.md) - Messages d'erreur en français

### Développement
- [`development_roadmap.md`](../docs/development_roadmap.md) - Roadmap de développement complet

### Refactorisation
- [`refactorisation_auth_separation.md`](docs/refactorisation_auth_separation.md) - Séparation HTML/CSS/JS pour Login et Signup
- [`CORRECTIONS_TEMPLATE.md`](docs/CORRECTIONS_TEMPLATE.md) - Corrections des templates
- [`REFACTORISATION_TEMPLATE_VERS_VUE.md`](docs/REFACTORISATION_TEMPLATE_VERS_VUE.md) - Refactorisation templates vers vues

---

## 🔍 Comment Utiliser Cette Documentation

### Pour Développeurs
1. **Commencer** : Lire [`development_roadmap.md`](../docs/development_roadmap.md) pour comprendre la vision
2. **Modifications** : Consulter [`CHANGELOG.md`](CHANGELOG.md) pour voir ce qui a été fait
3. **Améliorations** : Voir [`RECOMMANDATIONS_AMELIORATION.md`](RECOMMANDATIONS_AMELIORATION.md) pour les prochaines étapes
4. **Tests** : Vérifier [`TEST_REPORT.md`](TEST_REPORT.md) pour l'état des tests

### Pour Nouveaux Contributeurs
1. Lire [`readme.md`](readme.md) pour l'installation
2. Consulter [`CHANGELOG.md`](CHANGELOG.md) pour l'historique
3. Voir [`development_roadmap.md`](../docs/development_roadmap.md) pour la roadmap

---

## 📝 Convention de Nommage

### Fichiers de Documentation
- **`CHANGELOG.md`** : Journal des modifications
- **`*_REPORT.md`** : Rapports (tests, erreurs, etc.)
- **`*_STRATEGIE.md`** : Stratégies et plans
- **`*_GUIDE.md`** : Guides d'utilisation
- **`*_MOCKUP.md`** : Mockups et designs

### Format des Entrées dans CHANGELOG.md
```markdown
## 📅 YYYY-MM-DD

### 🔧 Corrections / ✨ Fonctionnalités / 📚 Documentation

#### [Numéro]. [Titre]
**Fichier(s)** : `chemin/fichier.py`
**Description** : ...
**Code** : ...
**Impact** : ...
**Statut** : ✅ / 🚧 / ❌
```

---

## 🔄 Mise à Jour de la Documentation

### Quand Documenter ?
- ✅ Après chaque correction de bug
- ✅ Après chaque nouvelle fonctionnalité
- ✅ Après chaque modification importante
- ✅ Après chaque série de tests
- ✅ Quand la stratégie change

### Où Documenter ?
- **Modifications** → `CHANGELOG.md`
- **Tests** → `TEST_REPORT.md`
- **Nouvelles fonctionnalités** → Créer un fichier dans `/docs` + mettre à jour `CHANGELOG.md`
- **Guides** → Créer dans `/docs`

---

## 📊 État Actuel de la Documentation

| Document | Statut | Dernière MAJ |
|----------|--------|--------------|
| CHANGELOG.md | ✅ À jour | 2025-01-27 |
| TEST_REPORT.md | ✅ À jour | 2025-01-27 |
| RECOMMANDATIONS_AMELIORATION.md | ✅ À jour | 2025-01-27 |
| PRIORISATION_STRATEGIE.md | ✅ À jour | 2025-01-27 |
| development_roadmap.md | ✅ À jour | 2025-12-01 |

---

## 🎯 Prochaines Documentations à Créer

Selon les fonctionnalités à venir :

1. **`docs/messagerie_implementation.md`** - Quand la messagerie sera implémentée
2. **`docs/paiement_stripe_guide.md`** - Quand le paiement sera implémenté
3. **`docs/notifications_system.md`** - Quand les notifications seront implémentées
4. **`docs/api_documentation.md`** - Documentation de l'API REST

---

## 🛠️ Scripts de Debug et Utilitaires

Tous les scripts de debug et utilitaires sont organisés dans le dossier [`scripts/`](scripts/README.md) :

- **`scripts/README.md`** - Documentation des scripts
- **`scripts/debug_*.py`** - Scripts de debug pour URLs et vues
- **`scripts/check_database.py`** - Vérification de la base de données
- **`scripts/create_*.py`** - Scripts de création (admin, utilisateurs de test)

Pour plus d'informations, consultez [`scripts/README.md`](scripts/README.md).

---

**Dernière mise à jour** : 2025-01-27 (Organisation fichiers debug)  
**Maintenu par** : Équipe de développement MentorXHub

