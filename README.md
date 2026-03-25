# Tontine API 🌍 — Gestion de Tontine Africaine

![Django](https://img.shields.io/badge/Django-6.0-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Système de gestion de tontine africaine développé avec Django et PostgreSQL.

> La tontine est un système d'épargne collectif traditionnel très répandu
> en Afrique de l'Ouest. Des membres d'un groupe cotisent régulièrement
> et chacun reçoit à tour de rôle la totalité des cotisations.

## 🌐 Portfolio
**https://oura02.pythonanywhere.com**

## 🚀 Fonctionnalités
- Gestion des groupes de tontine
- Gestion des membres et adhésions
- Cycles de cotisations avec bénéficiaire désigné
- Suivi des paiements (espèces, mobile money, virement)
- Confirmation et historique des paiements
- Statistiques par groupe et par cycle
- Détection des paiements en retard
- API REST complète avec JWT
- Interface admin Django

## 🛠️ Technologies
- Python 3.12 / Django 6.0
- Django REST Framework
- JWT Authentication (SimpleJWT)
- PostgreSQL 18
- django-filter

## ⚙️ Installation
git clone https://github.com/oura02/tontine.git
cd tontine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Configurer PostgreSQL dans settings.py :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'monprojet_db',
        'USER': 'postgres',
        'PASSWORD': 'Ou1985Ra1985@',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## 📡 Endpoints API
- POST /api/token/ — Obtenir le token JWT
- GET/POST /api/groupes/ — Groupes de tontine
- GET /api/groupes/{id}/statistiques/ — Stats du groupe
- GET /api/groupes/{id}/membres/ — Membres du groupe
- GET/POST /api/membres/ — Membres
- GET/POST /api/adhesions/ — Adhésions
- GET/POST /api/cycles/ — Cycles de cotisations
- POST /api/cycles/{id}/terminer/ — Terminer un cycle
- GET/POST /api/paiements/ — Paiements
- POST /api/paiements/{id}/confirmer/ — Confirmer paiement
- GET /api/paiements/en_retard/ — Paiements en retard
- GET /api/paiements/statistiques/ — Statistiques

## 📁 Structure
tontine/
├── membres/       # Groupes, membres, adhésions
├── cotisations/   # Cycles de cotisations
└── paiements/     # Paiements et bénéfices

## 🔗 Liens
- Portfolio : https://oura02.pythonanywhere.com
- GitHub : https://github.com/oura02
- LinkedIn : https://linkedin.com/in/romeo-konan-oura-0aa31086

## 👨‍💻 Auteur
KONAN ROMEO OURA
Développeur Python/Django Senior — Freelance
Abidjan, Côte d'Ivoire 🇨🇮
Volontaire DjangoCon Europe 2026 — Athènes, Grèce 🌍
