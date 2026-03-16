# Parcours d'Inscription Utilisateur - MentorXHub

## 📱 Page d'Inscription Actuelle (Sans Google OAuth)

Lorsqu'un utilisateur clique sur "S'inscrire" ou visite `/accounts/signup/`, voici ce qu'il voit :

### Design Visuel

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗ │
│  ║                    PANNEAU GAUCHE (45%)                   ║ │
│  ║  ╔════════════════════════════════════════════════════╗   ║ │
│  ║  ║  🅼  MentorXHub                                    ║   ║ │
│  ║  ╚════════════════════════════════════════════════════╝   ║ │
│  ║                                                           ║ │
│  ║                                                           ║ │
│  ║  Créez votre compte                                       ║ │
│  ║  Rejoignez notre communauté d'apprenants ambitieux        ║ │
│  ║                                                           ║ │
│  ║                                                           ║ │
│  ║  ┌─────────────────────────────────────────────┐         ║ │
│  ║  │  Vous avez déjà un compte ?                │         ║ │
│  ║  │                                             │         ║ │
│  ║  │  [ Se connecter ]                           │         ║ │
│  ║  └─────────────────────────────────────────────┘         ║ │
│  ║                                                           ║ │
│  ║  (Fond: Dégradé bleu foncé, cercles animés)             ║ │
│  ╚═══════════════════════════════════════════════════════════╝ │
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗ │
│  ║              PANNEAU DROITE (55%) - FORMULAIRE            ║ │
│  ║  ┌─────────────────────────────────────────────────────┐ ║ │
│  ║  │ Prénom *          │ Nom *                           │ ║ │
│  ║  │ [─────────────]   │ [─────────────]                 │ ║ │
│  ║  └─────────────────────────────────────────────────────┘ ║ │
│  ║                                                           ║ │
│  ║  Adresse email *                                          ║ │
│  ║  [──────────────────────────────────────────────────────] ║ │
│  ║                                                           ║ │
│  ║  Je veux être *                                           ║ │
│  ║  ┌─────────────────┐  ┌─────────────────┐               ║ │
│  ║  │   ○ Mentoré     │  │   ○ Mentor      │               ║ │
│  ║  └─────────────────┘  └─────────────────┘               ║ │
│  ║                                                           ║ │
│  ║  Mot de passe *         Confirmez *                       ║ │
│  ║  [─────────────] 👁️    [─────────────] 👁️               ║ │
│  ║                                                           ║ │
│  ║  [      Créer mon compte      ]                          ║ │
│  ║                                                           ║ │
│  ║  (Fond: Bleu très pâle #eff6ff)                          ║ │
│  ╚═══════════════════════════════════════════════════════════╝ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Détails du Design Actuel

**Panneau Gauche** :
- Fond : Dégradé bleu foncé (#1D4ED8 → #1E3A8A → #0F172A)
- Logo "M" dans un carré arrondi blanc semi-transparent
- Titre : "Créez votre compte"
- Sous-titre : "Rejoignez notre communauté d'apprenants ambitieux"
- Box translucide avec lien "Se connecter"
- Cercles animés en arrière-plan (effet de flottement)

**Panneau Droite** :
- Fond : Bleu très pâle (#eff6ff)
- Champs blancs (#ffffff)
- Inputs avec coins arrondis
- Boutons carrés bleus pour voir le mot de passe
- Sélecteur de rôle (2 cartes interactives)
- Bouton bleu "Créer mon compte"

---

## 🔄 Nouveau Parcours AVEC Google OAuth

### Scénario 1 : Inscription Classique (Inchangé)

L'utilisateur remplit tous les champs → Même comportement qu'actuellement.

---

### Scénario 2 : Inscription avec Google (NOUVEAU)

#### 📍 Étape 1 : Page Signup Modifiée

```
┌─────────────────────────────────────────────────────────────────┐
│                   PANNEAU DROITE - FORMULAIRE                   │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  🔵🔴🟡🟢  Continuer avec Google                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           ═══ OU ═══                            │
│                                                                 │
│  Prénom *            Nom *                                      │
│  [─────────────]     [─────────────]                           │
│                                                                 │
│  Adresse email *                                                │
│  [──────────────────────────────────────────────────────────]  │
│                                                                 │
│  Je veux être *                                                 │
│  ┌─────────────────┐  ┌─────────────────┐                     │
│  │   ○ Mentoré     │  │   ○ Mentor      │                     │
│  └─────────────────┘  └─────────────────┘                     │
│                                                                 │
│  Mot de passe *         Confirmez *                            │
│  [─────────────] 👁️    [─────────────] 👁️                    │
│                                                                 │
│  [      Créer mon compte      ]                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Changements** :
- ✨ **Bouton Google** en haut, blanc avec logo Google
- 📏 **Séparateur "OU"** élégant
- 📝 **Formulaire classique** en dessous (pour ceux qui préfèrent)

---

#### 📍 Étape 2 : Utilisateur Clique sur "Continuer avec Google"

**Action** : Redirection vers Google pour l'authentification.

**Écran Google** :
```
┌─────────────────────────────────────────┐
│         🔵 Google Sign In               │
│                                         │
│  Choisissez un compte                   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 👤 John Doe                     │   │
│  │    john.doe@gmail.com           │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 👤 Jane Smith                   │   │
│  │    jane.smith@gmail.com         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [ + Utiliser un autre compte ]        │
│                                         │
└─────────────────────────────────────────┘
```

---

#### 📍 Étape 3 : Autorisation Google

```
┌─────────────────────────────────────────┐
│  MentorXHub souhaite accéder à :        │
│                                         │
│  ✅ Votre email                         │
│  ✅ Votre nom et photo de profil        │
│                                         │
│  [ Annuler ]    [ Autoriser ]           │
└─────────────────────────────────────────┘
```

---

#### 📍 Étape 4 : Page de Sélection du Rôle ⭐ NOUVEAU

**URL** : `/accounts/select-role/`

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                Bienvenue sur MentorXHub !                       │
│             Pour continuer, veuillez choisir votre rôle         │
│                                                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────┐     │
│  │         🎓              │  │         📚              │     │
│  │                         │  │                         │     │
│  │   Je suis Mentor        │  │   Je suis Étudiant      │     │
│  │                         │  │                         │     │
│  │  Je souhaite partager   │  │  Je cherche un mentor   │     │
│  │  mon expérience et      │  │  pour m'accompagner     │     │
│  │  guider des étudiants   │  │  dans mon parcours      │     │
│  │                         │  │                         │     │
│  └─────────────────────────┘  └─────────────────────────┘     │
│          (Cliquable)                  (Cliquable)              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                     [ Continuer ]                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Design** :
- 🎨 Fond blanc avec carte centrale
- 🔵 Dégradé de fond violet-bleu
- 💎 2 grandes cartes élégantes (Mentor / Étudiant)
- ✨ Animation au survol : carte remonte légèrement
- ✅ Carte sélectionnée : bordure bleue + fond bleu clair
- 🔘 Gros bouton "Continuer" en bas

**Expérience utilisateur** :
1. Les 2 cartes sont côte à côte
2. L'utilisateur clique sur l'une d'elles
3. La carte s'illumine (bordure bleue, fond teinté)
4. Le bouton "Continuer" devient actif
5. Clic sur "Continuer" → **Compte créé !**

---

#### 📍 Étape 5 : Redirection vers le Dashboard

**URL** : `/` (home)

L'utilisateur est connecté automatiquement et redirigé vers :
- **Dashboard Étudiant** (si role = student)
- **Dashboard Mentor** (si role = mentor)

Message de bienvenue :
```
✅ Bienvenue John Doe ! Votre compte a été créé avec succès.
```

---

## 📊 Comparaison des 2 Parcours

### Inscription Classique (Actuelle)

```
Page Signup
    ↓
Remplir 6 champs (Prénom, Nom, Email, Rôle, MdP, Confirm)
    ↓
Cliquer "Créer mon compte"
    ↓
✅ Compte créé & connecté
    ↓
Dashboard
```

**Temps estimé** : 2-3 minutes  
**Nombre de clics** : ~15 (saisie de tous les champs)

---

### Inscription Google OAuth (Nouveau)

```
Page Signup
    ↓
Clic "Continuer avec Google"
    ↓
Popup Google (choisir compte)
    ↓
Clic "Autoriser"
    ↓
Page Sélection Rôle
    ↓
Clic sur carte Mentor/Étudiant
    ↓
Clic "Continuer"
    ↓
✅ Compte créé & connecté
    ↓
Dashboard
```

**Temps estimé** : 15-30 secondes  
**Nombre de clics** : 4 (Google → Autoriser → Rôle → Continuer)

---

## 🎨 Mockup Visuel de la Page Signup Finale

```
┌─────────────────────────────────────────────────────────────────┐
│ ╔═══════════════════════╗  ╔═══════════════════════════════╗   │
│ ║   PANNEAU GAUCHE      ║  ║   PANNEAU DROITE (Formulaire) ║   │
│ ║   (45%)               ║  ║   (55%)                       ║   │
│ ║                       ║  ║                               ║   │
│ ║ 🅼  MentorXHub        ║  ║ ┌───────────────────────────┐ ║   │
│ ║                       ║  ║ │ 🔵🔴🟡🟢 Google          │ ║   │
│ ║ Créez votre compte    ║  ║ └───────────────────────────┘ ║   │
│ ║ Rejoignez notre       ║  ║                               ║   │
│ ║ communauté...         ║  ║        ═══ OU ═══             ║   │
│ ║                       ║  ║                               ║   │
│ ║ ┌───────────────────┐ ║  ║ Prénom *    │ Nom *          ║   │
│ ║ │ Déjà un compte ?  │ ║  ║ [────────]  │ [────────]     ║   │
│ ║ │ [ Se connecter ]  │ ║  ║                               ║   │
│ ║ └───────────────────┘ ║  ║ Email *                       ║   │
│ ║                       ║  ║ [──────────────────────────]  ║   │
│ ║ (Cercles animés)     ║  ║                               ║   │
│ ║                       ║  ║ Je veux être *                ║   │
│ ║                       ║  ║ [Mentoré] [Mentor]            ║   │
│ ║                       ║  ║                               ║   │
│ ╚═══════════════════════╝  ║ MdP *    │ Confirm *         ║   │
│                            ║ [─────]👁️│ [─────]👁️         ║   │
│                            ║                               ║   │
│                            ║ [  Créer mon compte  ]        ║   │
│                            ╚═══════════════════════════════╝   │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Avantages de Google OAuth

### Pour l'Utilisateur :
- ⚡ **Inscription ultra-rapide** (30 secondes vs 3 minutes)
- 🔒 **Sécurité** : Pas besoin de créer un nouveau mot de passe
- ✅ **Email vérifié** automatiquement (pas de confirmation par email)
- 🎯 **Moins de friction** : 4 clics au lieu de 15

### Pour MentorXHub :
- 📈 **Taux de conversion** plus élevé (moins d'abandon)
- ✉️ **Données fiables** : Emails Gmail valides
- 🚫 **Moins de spam** : Comptes Google = vrais utilisateurs
- 💼 **Professionnel** : Standard de l'industrie

---

## 🔄 Flux Complet (Diagramme)

```
┌─────────────────────────────────────────────────────────────┐
│                    UTILISATEUR ARRIVE                       │
│                         SUR SIGNUP                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
    ┌───▼────┐                  ┌─────▼─────┐
    │ Google │                  │ Formulaire│
    │  OAuth │                  │  Classique│
    └───┬────┘                  └─────┬─────┘
        │                             │
┌───────▼────────┐            ┌───────▼────────┐
│ Popup Google   │            │ Remplir tous   │
│ Autorisation   │            │ les champs     │
└───────┬────────┘            └───────┬────────┘
        │                             │
┌───────▼────────┐                    │
│ Select Role    │                    │
│  Page          │                    │
└───────┬────────┘                    │
        │                             │
        │                             │
        └──────────┬──────────────────┘
                   │
         ┌─────────▼──────────┐
         │  COMPTE CRÉÉ       │
         │  + CONNEXION AUTO  │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │    DASHBOARD       │
         │  (Home ou Mentor)  │
         └────────────────────┘
```

---

## 📋 Points Clés à Retenir

1. **Page actuelle** : Formulaire classique en 2 panneaux (gauche = branding, droite = form)
2. **Bouton Google** : Ajouté en haut du formulaire, optionnel
3. **Page rôle** : Nouvelle page intermédiaire élégante pour choisir Mentor/Étudiant
4. **Fallback** : Le formulaire classique reste disponible (sans Google)
5. **UX optimale** : L'utilisateur choisit son parcours (rapide ou complet)

---

**Date de création** : 2025-12-01
