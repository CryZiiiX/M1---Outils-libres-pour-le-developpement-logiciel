# =============================================================================
# Fichier : back-end/app/models.py
# Rôle    : Définir le modèle ORM Prediction persisté en base (PostgreSQL/SQLite).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Modèles SQLAlchemy — table predictions.

Une ligne par prédiction avec inputs, modèle utilisé et résultats (LR/DT).
"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base


class Prediction(Base):
    """Enregistrement d'une prédiction de risque de crédit.

    Stocke les 11 features d'entrée, le modèle utilisé (lr/dt/both) et
    les résultats (probability, risk_level, credit_decision) pour LR et DT.
    """

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    person_age = Column(Integer, nullable=False)
    person_income = Column(Integer, nullable=False)
    person_home_ownership = Column(String, nullable=False)
    person_emp_length = Column(Float, nullable=False)
    loan_intent = Column(String, nullable=False)
    loan_grade = Column(String, nullable=False)
    loan_amnt = Column(Integer, nullable=False)
    loan_int_rate = Column(Float, nullable=False)
    loan_percent_income = Column(Float, nullable=False)
    cb_person_default_on_file = Column(String, nullable=False)
    cb_person_cred_hist_length = Column(Integer, nullable=False)
    model_used = Column(String, nullable=False)

    probability_lr = Column(Float, nullable=True)
    risk_level_lr = Column(String, nullable=True)
    credit_decision_lr = Column(String, nullable=True)
    probability_dt = Column(Float, nullable=True)
    risk_level_dt = Column(String, nullable=True)
    credit_decision_dt = Column(String, nullable=True)
