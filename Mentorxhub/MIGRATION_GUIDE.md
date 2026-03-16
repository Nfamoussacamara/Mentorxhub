# 🔧 Correction Migration - Guide Rapide

## ✅ Problème Résolu

La migration a été corrigée et renommée :
- ❌ ~~`0013_add_available_status_and_nullable_student.py`~~ (mauvaise dépendance)
- ✅ `0006_add_available_status_and_nullable_student.py` (dépend de `0005`)

---

## 🚀 Commandes à Exécuter

### 1. Appliquer la Migration

**Avec l'environnement virtuel actif :**
```bash
python manage.py migrate mentoring
```

**OU si l'env n'est pas activé :**
```bash
.\mon_env\Scripts\activate
python manage.py migrate mentoring
```

---

### 2. Redémarrer le Serveur

```bash
python manage.py runserver
```

---

## ✅ Ce qui va se passer

La migration va :
1. ✅ Rendre le champ `student` nullable dans `MentoringSession`
2. ✅ Ajouter le nouveau status `'available'`

**Aucune perte de données !**

---

## 🎯 Tester les Sessions Ouvertes

Une fois le serveur relancé :

### **En tant que MENTOR :**
1. Allez sur : `http://127.0.0.1:8000/mentoring/mentor/sessions/create-available/`
2. Créez une session **sans sélectionner d'étudiant**
3. La session apparaîtra avec status "Disponible"

### **En tant que ÉTUDIANT :**
1. Allez sur : `http://127.0.0.1:8000/mentoring/available-sessions/`
2. Vous verrez toutes les sessions ouvertes
3. Cliquez "Réserver" sur une session
4. ✅ Session confirmée instantanément !

---

## 📊 Vérifier que Tout Fonctionne

```bash
# Liste des migrations appliquées
python manage.py showmigrations mentoring

# Devrait afficher :
# [X] 0001_initial
# [X] 0002_alter_studentprofile_github_profile_and_more
# [X] 0003_mentorprofile_status
# [X] 0004_subject_studentprofile_interests_old_and_more
# [X] 0005_alter_mentoringsession_status
# [X] 0006_add_available_status_and_nullable_student
```

---

**Tout est prêt ! 🎊**
