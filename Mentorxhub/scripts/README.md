# Scripts de Debug et Utilitaires

Ce dossier contient tous les scripts de debug et utilitaires du projet MentorXHub.

## 📁 Contenu

### Scripts de Debug

- **`debug_reverse.py`** - Test des URLs avec `reverse()` Django
- **`debug_reverse_shell.py`** - Version shell pour tester `reverse()`
- **`debug_view.py`** - Test des vues Django
- **`debug_view_shell.py`** - Version shell pour tester les vues

### Scripts Utilitaires

- **`check_database.py`** - Vérification de l'état de la base de données
- **`create_admin.py`** - Création d'un superutilisateur admin
- **`create_test_user.py`** - Création d'utilisateurs de test

### Fichiers de Log

- **`error_log.html`** - Logs d'erreurs HTML (si généré)

## 🚀 Utilisation

Pour exécuter un script, utilisez :

```bash
python scripts/nom_du_script.py
```

Ou depuis le répertoire racine du projet :

```bash
cd D:\Mentorxhub\Mentorxhub
python scripts/nom_du_script.py
```

## ⚠️ Note

Ces scripts sont destinés au développement et au debug. Ils ne doivent pas être utilisés en production.

