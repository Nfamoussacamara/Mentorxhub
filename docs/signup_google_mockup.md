# Maquette Page d'Inscription avec Google OAuth - MentorXHub

## Vue d'ensemble

Cette maquette présente la nouvelle page d'inscription de MentorXHub avec l'intégration de **Google Sign-In** comme méthode d'inscription principale, tout en conservant l'option d'inscription traditionnelle par email.

---

## Layout Principal

### Structure : Split-Screen (45% / 55%)

```
┌─────────────────────────────────────────────────────────────┐
│                    │                                        │
│   PANNEAU GAUCHE   │         PANNEAU DROIT                  │
│     (45%)          │           (55%)                        │
│   Branding +       │      Formulaire d'inscription          │
│   Information      │                                        │
│                    │                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Panneau Gauche (45%) - Zone de Branding

### Fond et Décoration
- **Gradient principal** : 
  - Top : `#1D4ED8` (Bleu profond)
  - Middle : `#1E3A8A` (Bleu moyen)
  - Bottom : `#0F172A` (Bleu très foncé/noir)
- **Effets décoratifs** :
  - Cercles flottants avec effet de glow (rgba semi-transparents)
  - Motifs géométriques subtils (triangles et cercles en SVG)
  - Animation de flottement lente et fluide

### Contenu

#### 1. En-tête (Logo)
```
┌─────────────────────┐
│  [M]  MentorXHub   │  ← Logo carré "M" + Nom
└─────────────────────┘
```
- Icône carrée : fond blanc semi-transparent, lettre "M" blanche, coin arrondi
- Texte "MentorXHub" : blanc, bold, 24px

#### 2. Contenu Principal (Centré verticalement)
- **Titre** : "Créez votre compte"
  - Couleur : Blanc
  - Taille : 36px
  - Poids : Bold (700)
  - Espacement : margin-bottom 1rem

- **Sous-titre** : "Rejoignez notre communauté d'apprenants ambitieux"
  - Couleur : Blanc à 95% opacité
  - Taille : 18px
  - Espacement : margin-bottom 3rem

#### 3. Boîte de Connexion (En bas)
```
┌──────────────────────────────────────┐
│  Vous avez déjà un compte ?         │
│  ┌──────────────────┐               │
│  │  Se connecter    │  ← Bouton     │
│  └──────────────────┘               │
└──────────────────────────────────────┘
```
- Fond : Blanc semi-transparent avec backdrop-filter blur
- Bordure : 1px blanc semi-transparent
- Coins arrondis : 16px
- Bouton blanc avec texte bleu

---

## 📝 Panneau Droit (55%) - Formulaire

### Fond
- Couleur : `#eff6ff` (Bleu très très clair)
- Padding généreux
- Scrollable si contenu déborde

### Contenu du Formulaire (De haut en bas)

#### 1. ⭐ BOUTON GOOGLE SIGN-IN (PRIORITAIRE)

```
┌────────────────────────────────────────────────────┐
│  [G]  Continuer avec Google                       │
└────────────────────────────────────────────────────┘
```

**Caractéristiques** :
- **Position** : Tout en haut du formulaire
- **Largeur** : 100% (full width)
- **Style** :
  - Fond : Blanc (`#FFFFFF`)
  - Bordure : `1px solid #E5E7EB`
  - Ombre : `0 2px 8px rgba(0, 0, 0, 0.1)`
  - Coins arrondis : `12px`
  - Padding : `1rem 1.5rem`
- **Icône Google** :
  - Logo Google multicolore (les 4 couleurs : bleu, rouge, jaune, vert)
  - Position : À gauche avec gap de 12px
  - Taille : 24px × 24px
- **Texte** :
  - Contenu : "Continuer avec Google"
  - Couleur : `#374151` (Gris foncé)
  - Taille : 16px
  - Poids : 600 (Semi-bold)
  - Centré verticalement
- **État Hover** :
  - Fond : `#F9FAFB`
  - Ombre : `0 4px 12px rgba(0, 0, 0, 0.15)`
  - Transform : `translateY(-2px)`
  - Transition : `all 0.3s ease`

#### 2. SÉPARATEUR

```
────────────  ou inscrivez-vous avec email  ────────────
```

**Caractéristiques** :
- Ligne horizontale grise : `#E5E7EB`
- Texte centré : "ou inscrivez-vous avec email"
- Couleur texte : `#6B7280` (Gris moyen)
- Taille : 14px
- Margin : `2rem 0`

#### 3. CHAMPS DU FORMULAIRE TRADITIONNEL

##### a) Prénom et Nom (2 colonnes)
```
┌─────────────────────┐  ┌─────────────────────┐
│ Prénom *            │  │ Nom *               │
│ [Entrez prénom...] │  │ [Entrez nom...]     │
└─────────────────────┘  └─────────────────────┘
```

##### b) Email (Pleine largeur)
```
┌──────────────────────────────────────────────────┐
│ Adresse email *                                  │
│ [votre.email@exemple.com]                       │
└──────────────────────────────────────────────────┘
```

##### c) Sélecteur de Rôle (2 cartes)
```
Je veux être *

┌──────────────────┐  ┌──────────────────┐
│                  │  │                  │
│    Mentoré       │  │     Mentor       │
│                  │  │                  │
└──────────────────┘  └──────────────────┘
```

**Caractéristiques des cartes** :
- Fond : Gradient `#FFFFFF` vers `#F9FAFB`
- Bordure : `2px solid #E5E7EB`
- État sélectionné :
  - Bordure : `2px solid #2563EB`
  - Fond : Gradient avec teinte bleue
  - Box-shadow : `0 0 0 3px rgba(37, 99, 235, 0.1)`
- Hover :
  - Bordure : `#60A5FA`
  - Transform : `translateY(-2px)`
  - Ombre portée

##### d) Mots de passe (2 colonnes avec boutons œil)
```
┌──────────────────────┐  ┌──────────────────────┐
│ Mot de passe *       │  │ Confirmez *          │
│ [••••••••]  [👁]    │  │ [••••••••]  [👁]    │
└──────────────────────┘  └──────────────────────┘
```

**Bouton œil** :
- Position : Bouton carré à droite
- Fond : `#2563EB` (Bleu)
- Couleur icône : Blanc
- Largeur : 48px
- Coins arrondis : 0 8px 8px 0
- Hover : `#1D4ED8`

#### 4. BOUTON DE SOUMISSION

```
┌────────────────────────────────────────────────────┐
│              Créer mon compte                      │
└────────────────────────────────────────────────────┘
```

**Caractéristiques** :
- Largeur : 100%
- Fond : `#2563EB` (Bleu)
- Couleur texte : Blanc
- Padding : `1rem`
- Coins arrondis : `12px`
- Ombre : `0 4px 12px rgba(37, 99, 235, 0.3)`
- Poids : 600
- Taille : 16px
- Margin-top : `1.5rem`
- Hover :
  - Fond : `#1D4ED8`
  - Transform : `translateY(-2px)`
  - Ombre : `0 8px 20px rgba(37, 99, 235, 0.4)`

---

## 🎯 Points Clés du Design

### Hiérarchie Visuelle
1. **Google Sign-In** = CTA primaire (le plus visible)
2. **Séparateur** = Distinction claire entre méthodes
3. **Formulaire email** = Alternative complète

### Palette de Couleurs
- **Bleu Principal** : `#2563EB`
- **Bleu Hover** : `#1D4ED8`
- **Bleu Clair** : `#60A5FA`
- **Fond Clair** : `#eff6ff`
- **Gris Bordure** : `#E5E7EB`
- **Gris Texte** : `#374151`, `#6B7280`

### Typographie
- **Police** : Inter (Google Fonts)
- **Poids** : 400 (Regular), 500 (Medium), 600 (Semi-bold), 700 (Bold)

### Effets et Animations
- **Transitions** : `all 0.3s ease`
- **Hover effects** : Transform + Shadow
- **Focus states** : Blue glow (`box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1)`)
- **Animations background** : Flottement lent (25s)

---

## 📱 Responsive Design

### Mobile (< 968px)
- **Layout** : Passage en colonne unique (vertical stack)
- **Panneau gauche** : Réduit, logo + titre uniquement
- **Panneau droit** : Pleine largeur
- **Colonnes formulaire** : Conversion en 1 colonne
- **Padding** : Réduit pour écrans plus petits

---

## 🔐 Fonctionnalités

### Google OAuth
1. Clic sur "Continuer avec Google"
2. Redirection vers authentification Google
3. Retour avec données utilisateur
4. Sélection du rôle (si nécessaire)
5. Création du compte automatique

### Inscription Email
1. Remplissage manuel du formulaire
2. Validation côté client (mots de passe identiques)
3. Soumission au backend Django
4. Validation serveur
5. Création du compte

---

## 💡 Améliorations UX

1. **Google en premier** : Encourage l'inscription rapide
2. **Séparateur clair** : Pas de confusion entre les méthodes
3. **Boutons œil** : Visibilité des mots de passe facile
4. **États visuels** : Hover, focus, selection bien définis
5. **Messages d'erreur** : Affichage clair sous chaque champ
6. **Design cohérent** : Maintien de la charte graphique existante

---

## 🚀 Prochaines Étapes d'Implémentation

1. Intégrer `django-allauth` pour Google OAuth
2. Configurer Google Cloud Console (Client ID & Secret)
3. Modifier le template `signup.html` 
4. Ajouter les routes Django pour le callback Google
5. Créer/adapter les signals pour synchronisation des données
6. Tester le flux complet d'inscription
7. Valider le design sur différents navigateurs et tailles d'écran
