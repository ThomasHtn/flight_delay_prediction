# ✈️ Flight Delay Predictor

--- 

## 📌 Contexte

Les retards de vols représentent un enjeu majeur pour les compagnies aériennes, les aéroports et les passagers. En 2019, 19 % des vols aux États-Unis ont été retardés, engendrant près de **28 milliards de dollars** de pertes économiques (source : *Bureau of Transportation Statistics*). Ces retards sont dus à de nombreux facteurs : conditions météo, trafic aérien, problèmes techniques, etc.

Ce projet vise à **développer un modèle de machine learning** capable de prédire si un vol sera **retardé de plus de 15 minutes à l’arrivée**. Ce modèle s’inscrit dans une démarche d’industrialisation complète (ETL, monitoring, API, gestion des modèles).

*ETL = Extract, Transform, Load (en français : Extraire, Transformer, Charger)* *

---

## 🎯 Objectifs

- Prédire de manière binaire si un vol sera **retardé (>15 min)** à l'arrivée.
- Industrialiser le processus complet :
  - Pipeline ETL automatisé
  - Stockage et historisation des données
  - Entraînement et suivi du modèle (MLflow)
  - Déploiement via une API (FastAPI)
  - Interface utilisateur (Streamlit)
- Respect des contraintes **éthiques**, **RGPD** et **scalabilité** de l'infrastructure.

--- 

## 🧱 Architecture du projet

```
.
│
├── api/                   # API FastAPI pour servir les prédictions
├── app/                   # Application Streamlit
├── database/
│   ├── models/            # Définition des tables SQLAlchemy
│   ├── schemas/           # Schémas Pydantic
│   └── migrations/        # Scripts Alembic pour la gestion du schéma
├── etl/                   # Pipelines de traitement et ingestion des données
├── ml/
│   ├── training/          # Scripts d'entraînement
│   ├── prediction/        # Chargement du modèle et prédictions
│   └── evaluation/        # Évaluation et suivi des performances
├── mlruns/                # Dossiers MLflow pour le tracking des expériences
├── notebooks/             # Analyses exploratoires (EDA, visualisations)
├── docker/                # Dockerfiles et configuration pour déploiement
├── .env                   # Fichier d'environnement
├── requirements.txt       # Dépendances du projet
├── Dockerfile             # Image pour API ou Streamlit
├── docker-compose.yml     # Orchestration du projet
└── README.md              # Ce fichier
```

---

## ⚙️ Stack technique

- **Python 3.10+**
- **Pandas**, **Scikit-learn**, **XGBoost**
- **MLflow** pour le tracking
- **FastAPI** pour l’API REST
- **Streamlit** pour l’interface utilisateur
- **SQLite / PostgreSQL** avec **SQLAlchemy + Alembic**
- **Prefect** pour l’orchestration des pipelines ETL
- **Docker** & **Docker Compose** pour la conteneurisation
- **Grafana** pour visualiser les métriques hardware et de consomation
- **Kuma** pour alerter en cas de crash de l'application
- **Loguru** pour le suivi des logs
- **Optuna** pour optimisation des hypers-paramètres


---

## 🌐 Virtual environment

**Linux**
```batch
python3 -m venv .venv
source .venv/bin/activate
```

**MacOS-Windows**
```batch
python -m venv .venv
.venv\Scripts\activate
```

---

## 🚀 Lancement du projet

### 1. Cloner le dépôt

```batch
git clone https://github.com/ThomasHtn/flight-delay-predictor.git
cd flight-delay-predictor
```

### 2. Lancer avec Docker

```batch
docker-compose up --build
```

Cela démarre :
- L’API FastAPI
- L’interface utilisateur Streamlit
- La base de données
- MLflow UI (sur `http://localhost:5000`)

### 3. Accès aux services

- **API** : http://localhost:8000/docs
- **Interface Streamlit** : http://localhost:8501
- **MLflow UI** : http://localhost:5000

---

## Streamlit (front)
Depuis la racine du projet :
```batch
streamlit run app/main.py
```

---

## FastAPI (api)
Depuis la racine du projet :
```batch
uvicorn api.main:app --reload
```

---

## Monitoring (Grafana + prometheus)
Depuis le repertoire "monitoring" :
```batch
cd monitoring/
docker-compose up -d
```

Interface : 
Prometheus : http://localhost:9090
Grafana	http://localhost:3000

---

## ⚗️ Alembic

### Créer une nouvelle migration
Depuis la racine du projet :
```batch
alembic revision --autogenerate -m "nom de la migration"
```

### Appliquer la migration
Depuis la racine du projet :
```batch
alembic upgrade head
```

### Remplir la base de données
Depuis la racine du projet :
```batch
make populate-db
```
Cela va utiliser par défaut le fichier **"cleaned_data.csv"** pour remplir la base de données.

---

##  Mlflow

Lancer l'interface web

```batch
mlflow ui
``` 

Interface : http://localhost:5000