# ✈️ Flight Delay Predictor

---

## 📌 Contexte

Les retards de vols représentent un enjeu majeur pour les compagnies aériennes, les aéroports et les passagers. En 2019, **19 % des vols aux États-Unis** ont été retardés, causant près de **28 milliards de dollars** de pertes économiques (source : *Bureau of Transportation Statistics*). Ces retards sont dus à de nombreux facteurs : conditions météo, trafic aérien, problèmes techniques, etc.

Ce projet a pour objectif de **développer un modèle de machine learning** capable de prédire si un vol sera **retardé de plus de 15 minutes à l’arrivée**, dans une logique d’**industrialisation complète** (ETL, API, monitoring, MLOps).

---

## 🎯 Objectifs

- Prédire de manière **binaire** si un vol sera **retardé (>15 min)** à l'arrivée.
- Industrialiser le processus de bout en bout :
  - Pipeline ETL automatisé
  - Stockage et historisation des données
  - Entraînement, suivi et versioning du modèle (MLflow)
  - Déploiement via une API REST (FastAPI)
  - Interface utilisateur (Streamlit)
  - Monitoring système (Grafana / Prometheus)
- Respect des contraintes **éthiques**, **RGPD** et de **scalabilité**.

---

## 🧱 Architecture du projet


```
.
├── alembic.ini                                # Alembic configuration file for database migrations
├── api                                        # FastAPI backend for prediction service
│   ├── Dockerfile                             # Docker configuration for API
│   ├── endpoints                              # API route handlers
│   │   ├── health.py                          # Health check endpoint
│   │   ├── predict.py                         # Prediction endpoint using trained model
│   ├── main.py                                # FastAPI app entrypoint
│   ├── models                                 # Pydantic schemas for request/response models
│   │   └── schemas.py                         # Request/response data schemas
│   ├── requirements.txt                       # Python dependencies for API service
│   └── services                               # Core logic used by endpoints
│       └── prediction_service.py              # Model loading and prediction logic
├── app                                        # Streamlit application for UI
│   ├── Dockerfile                             # Docker configuration for Streamlit app
│   ├── main.py                                # Streamlit app entrypoint
│   └── requirements.txt                       # Python dependencies for Streamlit app
├── assets                                     # Generated performance plots and diagrams
│   ├── *.png                                  # Visual assets (MLflow, Docker, LightGBM, etc.)
├── data                                       # Raw and processed datasets
│   ├── processed
│   │   └── cleaned_data.csv                   # Cleaned and preprocessed dataset
│   └── raw                                    # Original CSV data (monthly)
│       ├── 2016_MM.csv                        # Raw flight data from Jan to Dec
├── database                                   # Database models and migration logic
│   ├── base.py                                # SQLAlchemy base class
│   ├── __init__.py                            # Makes "database" a Python package
│   ├── migrations                             # Alembic migration scripts
│   │   ├── env.py                             # Alembic environment setup
│   │   ├── versions/*.py                      # Auto-generated migration scripts
│   ├── models                                 # SQLAlchemy models for each table
│   │   ├── airline.py                         # Airline table definition
│   │   ├── airports.py                        # Airports table definition
│   │   └── flight.py                          # Flights table definition
│   ├── schemas                                # Pydantic schemas for DB entities
│   │   └── flight.py                          # Flight-specific schema
│   └── services                               # Data access layer logic
│       └── flight_service.py                  # Queries for the flights dataset
├── docker-compose.yml                         # Orchestration file to run containers together
├── dump                                       # Contains local SQLite database dump
│   └── flights.db                             # SQLite database file
├── exploratory_data_analysis.ipynb            # Jupyter notebook for exploratory data analysis
├── journal-de-bord.ipynb                      # Project logbook / research notebook
├── Makefile                                   # Automation commands (build, test, etc.)
├── ml                                         # Machine learning logic
│   ├── evaluation
│   │   └── evaluate.py                        # Model evaluation script (metrics, plots)
│   ├── models_artifact                        # Pickled models and preprocessors
│   │   └── *.pkl                              # Serialized sklearn/LGBM models and preprocessors
│   └── training                               # Model training and preprocessing logic
│       ├── models.py                          # Model definitions and training logic
│       ├── preprocessing.py                   # Data preprocessing steps (encoders, pipelines)
│       └── train_model.py                     # Full training script with MLflow/Optuna
├── mlruns                                     # MLflow tracking folder (runs, metrics, models)
│   └── <experiment_id>/<run_id>               # Contains metrics, parameters, models for each run
├── monitoring                                 # Observability setup
│   ├── grafana                                # Grafana dashboards and config
│   └── prometheus                             # Prometheus scraping config
├── README.md                                  # Project overview and documentation
├── requirements.txt                           # Project-wide dependencies
├── scripts                                    # One-off or utility scripts
│   └── clear_and_populate_db.py               # Initialize and populate the database
└── tests                                      # Unit and integration tests
    └── test_flight_service.py                 # Tests for the flight service logic
```
---

## ⚙️ Stack technique

- **Python 3.10+**
- **Pandas**, **Scikit-learn**, **LightGBM**
- **MLflow** pour le suivi des expérimentations
- **Optuna** pour l’optimisation des hyperparamètres
- **FastAPI** pour l’API de prédiction
- **Streamlit** pour l’interface utilisateur
- **SQLite / PostgreSQL** via **SQLAlchemy** et **Alembic**
- **Docker** & **Docker Compose** pour la conteneurisation
- **Grafana + Prometheus** pour le monitoring des services

---

## 🌐 Environnement virtuel

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

---

## 🚀 Lancement du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/ThomasHtn/flight-delay-predictor.git
cd flight-delay-predictor
```

### 2. Lancer avec Docker

```bash
docker-compose up --build
```

Cela démarre :
- L’API (FastAPI) sur http://0.0.0.0:8000/docs
- L’interface utilisateur (Streamlit) sur http://0.0.0.0:8501
- Le monitoring (Grafana) sur http://0.0.0.0:3000

---

## 📊 Monitoring

Lancer Prometheus & Grafana :

```bash
docker-compose up -d
```

- **Prometheus** : http://0.0.0.0:9090  
- **Grafana** : http://0.0.0.0:3000  

---

## 🧪 Lancer les tests

```bash
make test
```

Les tests sont situés dans le dossier `tests/`. Ils sont également exécutés automatiquement à chaque push sur la branche `main` via **GitHub Actions**.

---

## 🧬 Entraîner les modèles

```bash
make train
```

Cela entraîne trois modèles :
- `RandomForest`
- `LogisticRegression`
- `LightGBM`

Les modèles sont enregistrés dans :
- `ml/models_artifact/`
- et suivis dans l’interface MLflow : http://localhost:5000

---

## 📈 Évaluation des performances

```bash
make evaluate
```

Par défaut, cela évalue `lightgbm_model.pkl` et génère une **matrice de confusion** enregistrée dans `assets/`.

---

## 🧪 FastAPI (API REST)

Lancer l’API manuellement :

```bash
uvicorn api.main:app --reload
```

Ou via Makefile :

```bash
make start-api
```

---

## 🎛️ Streamlit (interface utilisateur)

Lancer l’interface manuellement :

```bash
streamlit run app/main.py
```

Ou via Makefile :

```bash
make start-app
```

---

## ⚗️ Alembic (migrations)

Créer une nouvelle migration :

```bash
alembic revision --autogenerate -m "nom de la migration"
```

Appliquer la migration :

```bash
alembic upgrade head
```

Remplir la base de données :

```bash
make clear-and-populate-db
```

Cela nettoie les CSV du dossier `data/raw/` et les insère dans la base de données SQLite.

---

## 📦 MLflow

Lancer l’interface MLflow :

```bash
mlflow ui
```

Interface : [http://localhost:5000](http://localhost:5000)

---

## ⚙️ GitHub Actions

Des pipelines CI/CD sont configurés :

- `test.yml` : exécute les tests Pytest
- `integration-check.yml` : vérifie que les conteneurs démarrent correctement
- `dockerhub.yml` : build et push automatique sur DockerHub

--- 

## 🖼️ Apperçu de l'application

**Streamlit**
![Streamlit](/assets/streamlit.png)

**Api de prediction**
![Api](/assets/api.png)

**Mlflow**
![Mlflow](/assets/mlflow.png)
![Mlflow](/assets/mlflow-details.png)
![Mlflow](/assets/mlflow-exploration.png)

**Lightgmb matrice de confusion**
![Lightgmb](/assets/lightgbm_confusion_matrix.png)

**Grafana**
![Grafana](/assets/grafana.png)

**Github actions**
![Actions](/assets/github-action.png)

**Docker hub**
![Docker](/assets/docker-hub.png)

