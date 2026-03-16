# Documentation du Projet MentorXHub

## Structure des Données

### Mentor
- **Nom**
- **Spécialité**
- **Bio**
- **Téléphone**
- **Ville**
- **Mentorés** (Clé étrangère)

### Mentoré
- **Nom**
- **Bio**
- **Téléphone**
- **Ville**
- **Technos**

### Session de Mentorat
- **Mentor**
- **Mentoré**
- **Heure de début**
- **Heure de fin**
- **Statut de la session**

### Disponibilité
- **ID Mentorat**
- **Jour de disponibilité**
- **Plage horaire**

### Avis
- **Mentor**
- **Mentoré**
- **Commentaire**

---

## Objectif du Projet
Mise en place d'un système d'authentification et de mise en relation pour les mentors et les mentorés.

### Processus d'Inscription Mentor
Lorsqu'un mentor souhaite rejoindre la plateforme, son compte n'est pas immédiatement visible. Notre équipe doit vérifier l'authenticité de son profil à travers des contrôles et entretiens pour garantir la qualité du service.

### Processus Mentoré
Une fois leur compte créé, les mentorés sont automatiquement guidés vers les mentors maîtrisant les technologies qu'ils souhaitent apprendre.

---

## Installation et Configuration (Windows)

### Problèmes Rencontrés et Solutions

#### 1. Environnements Virtuels Multiples
**Problème :** Présence de plusieurs environnements virtuels (`env`, `mon_env`) créés sur différents systèmes (Linux/Mac vs Windows) causant des conflits.

**Solution :**
- Suppression des environnements incompatibles
- Création d'un environnement virtuel propre pour Windows :
```powershell
cd d:\Mentorxhub\Mentorxhub
python -m venv mon_env
```

#### 2. Erreur d'Installation de Pillow
**Problème :** Pillow 11.1.0 ne supporte pas Python 3.14 et nécessite la compilation depuis les sources sur Windows (erreur zlib).

**Erreur rencontrée :**
```
RequiredDependencyException: zlib
The headers or library files could not be found for zlib
Pillow 11.1.0 does not support Python 3.14 and does not provide prebuilt Windows binaries
```

**Solution :**
- Installation de la version la plus récente de Pillow (12.0.0) qui fournit des binaires précompilés pour Python 3.14 :
```powershell
pip install Django==5.1.7 asgiref==3.8.1 sqlparse==0.5.3 Pillow
```

#### 3. Conflit de Chemins (OneDrive vs Disque Local)
**Problème :** L'environnement virtuel pointait vers `C:\Users\camar\OneDrive\Mentorxhub\` au lieu de `D:\Mentorxhub\`.

**Solution :**
- Recréation complète de l'environnement virtuel dans le bon répertoire ci-dessous.

### Commandes d'Installation
```powershell
# 1. Créer l'environnement virtuel
python -m venv mon_env

# 2. Installer les dépendances
.\mon_env\Scripts\pip.exe install Django==5.1.7 asgiref==3.8.1 sqlparse==0.5.3 Pillow

# 3. Lancer le serveur
.\mon_env\Scripts\python.exe manage.py runserver
```

### Accès au Projet
Le serveur de développement est accessible à l'adresse : **http://127.0.0.1:8000/**

---

## 📚 Documentation

### Documentation Principale
- **[CHANGELOG.md](CHANGELOG.md)** - Journal de toutes les modifications et corrections
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Index complet de la documentation
- **[TEST_REPORT.md](TEST_REPORT.md)** - Rapport des tests effectués
- **[RECOMMANDATIONS_AMELIORATION.md](RECOMMANDATIONS_AMELIORATION.md)** - Recommandations d'amélioration
- **[PRIORISATION_STRATEGIE.md](PRIORISATION_STRATEGIE.md)** - Stratégie de développement

### Documentation Technique
Toute la documentation technique se trouve dans le dossier [`docs/`](../docs/) :
- Roadmap de développement
- Guides d'implémentation
- Documentation des fonctionnalités

**Voir [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) pour la liste complète.**
