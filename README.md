# WacStaff

[![Démo en ligne](https://img.shields.io/badge/Démo-wacstaff.onrender.com-4A90D9?style=for-the-badge&logo=render&logoColor=white)](https://wacstaff.onrender.com/WacStaff/login/)

Application web de gestion du personnel et des affectations pour la chaîne de restaurants fictive **WACDO**.

---

## Objectif

Projet réalisé dans le cadre de ma formation développeur fullstack Python/Django.
L'objectif était de créer une application métier réaliste avec :
- gestion utilisateurs
- RBAC
- déploiement production
- tests automatisés

---

## Fonctionnalités

- **Gestion des collaborateurs** — Création, modification, désactivation (soft delete via `is_active`)
- **Gestion des restaurants et fonctions** — CRUD complet
- **Affectations** — Lien collaborateur ↔ restaurant ↔ fonction avec dates de début/fin
- **Authentification par email** — Modèle utilisateur personnalisé (`AbstractBaseUser`)
- **RBAC** — Accès différencié selon le rôle (`is_staff`, superuser)
- **Interface** — Héritage de templates, modales de confirmation, messages flash auto-dismiss

---

## Stack technique

| Couche | Technologie |
|---|---|
| Backend | Python / Django |
| Base de données | PostgreSQL (Render) |
| Fichiers statiques | WhiteNoise |
| Serveur WSGI | Gunicorn |
| Déploiement | Render |

---

## Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/Kolwaan/PROJET_DJANGO.git
cd PROJET_DJANGO

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# Renseigner SECRET_KEY, DATABASE_URL, DEBUG=True

# Migrations et seed
python projet_django/manage.py migrate
python projet_django/manage.py seed

# Lancer le serveur
python projet_django/manage.py runserver
```

---

## Déploiement (Render)

**Build command :**
```bash
pip install -r requirements.txt \
  && python projet_django/manage.py collectstatic --noinput \
  && python projet_django/manage.py migrate \
  && python projet_django/manage.py seed
```

**Start command :**
```bash
gunicorn --chdir projet_django projet_django.wsgi
```

⚠️ Note : La base PostgreSQL gratuite Render peut être réinitialisée après une période d'inactivité.  
Les données de démonstration sont automatiquement recréées via la commande `seed`.

---

## Tests

```bash
python projet_django/manage.py test
```

La suite couvre : modèles, authentification, RBAC, filtre « non affectés », validation des formulaires — **15 tests** au total.

---

## Structure du projet

```
projet_django/
├── projet_django/       # Configuration Django (settings, urls, wsgi)
│   ├── settings.py
│   └── settings_prod.py
├── wacstaff/            # Application principale
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│       ├── wacstaff.css
│       └── wacstaff.js
└── manage.py
```

---

## Auteur

**Nicolas Colin** — Formation Développeur Fullstack Python/Django  
Global Digital University · Promotion 2026
