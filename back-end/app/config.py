"""Configuration de l'application Flask.

Variables d'environnement et chemins des modèles joblib.
BASE_DIR = back-end/, MODELS_DIR = back-end/models/.

Variables d'environnement :
    DATABASE_URL : Connexion SQLAlchemy. Défaut sqlite pour dev/test.
                   En Docker : postgresql://... fourni par docker-compose.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
LR_MODEL_PATH = MODELS_DIR / "logistic_regression.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
DT_MODEL_PATH = MODELS_DIR / "decision_tree.joblib"

# sqlite par défaut (dev/test) ; PostgreSQL en prod via docker-compose
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./predictions.db"
)
