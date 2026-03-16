# 🧪 Instructions de Test - Phase 1

## ✅ Configuration Vérifiée

- ✅ Application `dashboard` créée
- ✅ Ajoutée dans `INSTALLED_APPS`
- ✅ URLs configurées
- ✅ Templates créés
- ✅ CSS et JavaScript créés
- ✅ Serveur en cours d'exécution en arrière-plan

---

## 🚀 Tests à Effectuer Maintenant

### 1. Ouvrir le Navigateur

Allez sur : **http://127.0.0.1:8000/dashboard/**

### 2. Test Sans Connexion

**Attendu** : Redirection vers la page de connexion

### 3. Test Avec Connexion (Mentor)

1. Connectez-vous avec un compte mentor
2. Allez sur : **http://127.0.0.1:8000/dashboard/**

**Vérifiez** :
- ✅ Sidebar visible à gauche avec navigation mentor
- ✅ Navbar en haut avec avatar
- ✅ 4 cartes de statistiques (Demandes, Sessions, Note, Revenus)
- ✅ Section "Prochaines Sessions"

### 4. Test Avec Connexion (Étudiant)

1. Connectez-vous avec un compte étudiant
2. Allez sur : **http://127.0.0.1:8000/dashboard/**

**Vérifiez** :
- ✅ Sidebar visible à gauche avec navigation étudiant
- ✅ Navbar en haut avec avatar
- ✅ 3 cartes de statistiques (Heures, Sessions, Mentors actifs)
- ✅ Section "Prochaines Sessions"
- ✅ Section "Mentors Recommandés"

### 5. Test des Fonctionnalités

#### Sidebar
- [ ] Cliquer sur le bouton hamburger (mobile) → Sidebar s'ouvre/ferme
- [ ] Navigation fonctionne (liens cliquables)

#### Navbar
- [ ] Cliquer sur l'avatar → Menu déroulant s'ouvre
- [ ] Appuyer sur `Ctrl+K` → Barre de recherche s'ouvre
- [ ] Cliquer sur l'icône de notifications → Dropdown s'ouvre

#### Theme Toggle
- [ ] Dans le menu utilisateur, cliquer sur "Mode sombre"
- [ ] Vérifier que le thème change
- [ ] Recharger la page → Le thème est conservé

#### Responsive
- [ ] Réduire la fenêtre à < 1024px
- [ ] Vérifier que la sidebar devient un drawer
- [ ] Vérifier que le layout s'adapte

---

## 🐛 Si Vous Voyez des Erreurs

### Erreur : Template not found
**Solution** : Vérifiez que les fichiers sont dans `templates/dashboard/`

### Erreur : Static files not found
**Solution** : Exécutez `python manage.py collectstatic`

### Erreur : Module dashboard not found
**Solution** : Vérifiez que `dashboard` est dans `INSTALLED_APPS` de `settings.py`

### Erreur : CSS ne se charge pas
**Solution** : Videz le cache du navigateur (Ctrl+F5)

---

## ✅ Checklist de Validation

- [ ] Serveur démarre sans erreur
- [ ] Dashboard accessible après connexion
- [ ] Sidebar visible et fonctionnelle
- [ ] Navbar visible avec tous les éléments
- [ ] Statistiques affichées correctement
- [ ] Navigation selon le rôle fonctionne
- [ ] Theme toggle fonctionne
- [ ] Responsive sur mobile
- [ ] Aucune erreur dans la console du navigateur (F12)

---

## 📸 Captures d'Écran Attendues

### Dashboard Mentor
- Sidebar avec : Dashboard, Demandes, Calendrier, Avis, Revenus, Paramètres
- 4 cartes statistiques
- Liste des prochaines sessions

### Dashboard Étudiant
- Sidebar avec : Dashboard, Trouver un Mentor, Mes Sessions, Messages, Favoris, Paramètres
- 3 cartes statistiques
- Liste des prochaines sessions
- Grille de mentors recommandés

---

**Une fois tous les tests validés, la Phase 1 est complète ! 🎉**

**Prochaine étape** : Phase 2 - Système AJAX/SPA

