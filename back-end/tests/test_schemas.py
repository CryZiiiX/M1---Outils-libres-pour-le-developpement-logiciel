# =============================================================================
# Fichier : back-end/tests/test_schemas.py
# Rôle    : Tester la validation Marshmallow : payloads valides, bornes
#           numériques, valeurs catégorielles, champs requis (7 tests).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Tests unitaires pour app.schemas (validation Marshmallow)."""
import pytest

from marshmallow import ValidationError

from app.schemas import PredictionInputSchema


VALID_PAYLOAD = {
    "person_age": 30,
    "person_income": 50000,
    "person_home_ownership": "RENT",
    "person_emp_length": 5,
    "loan_intent": "PERSONAL",
    "loan_grade": "B",
    "loan_amnt": 10000,
    "loan_int_rate": 10,
    "loan_percent_income": 0.2,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 5,
}


def test_schema_valid_payload():
    """Payload valide est accepté."""
    schema = PredictionInputSchema()
    result = schema.load(VALID_PAYLOAD)
    assert result["person_age"] == 30
    assert result["model_choice"] == "both"  # défaut


def test_schema_model_choice_optional():
    """model_choice est optionnel, défaut 'both'."""
    schema = PredictionInputSchema()
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "model_choice"}
    result = schema.load(payload)
    assert result.get("model_choice", "both") == "both"


def test_schema_age_out_of_range():
    """Âge hors bornes (18-100) → ValidationError."""
    schema = PredictionInputSchema()
    payload = {**VALID_PAYLOAD, "person_age": 17}
    with pytest.raises(ValidationError):
        schema.load(payload)
    payload["person_age"] = 101
    with pytest.raises(ValidationError):
        schema.load(payload)


def test_schema_invalid_categorical():
    """Valeur catégorielle invalide → ValidationError."""
    schema = PredictionInputSchema()
    payload = {**VALID_PAYLOAD, "person_home_ownership": "INVALID"}
    with pytest.raises(ValidationError):
        schema.load(payload)
    payload = {**VALID_PAYLOAD, "loan_grade": "Z"}
    with pytest.raises(ValidationError):
        schema.load(payload)


def test_schema_missing_required():
    """Champ requis manquant → ValidationError."""
    schema = PredictionInputSchema()
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "person_age"}
    with pytest.raises(ValidationError):
        schema.load(payload)


def test_schema_loan_amnt_too_large():
    """loan_amnt géant (> 100 000) → ValidationError (400), pas une erreur 500.

    Sans borne max, une valeur au-delà de 2^31-1 passait la validation puis
    débordait la colonne Integer de PostgreSQL en production.
    """
    schema = PredictionInputSchema()
    payload = {**VALID_PAYLOAD, "loan_amnt": 3_000_000_000}
    with pytest.raises(ValidationError):
        schema.load(payload)
    payload["loan_amnt"] = 100_001
    with pytest.raises(ValidationError):
        schema.load(payload)


def test_schema_loan_percent_income_out_of_range():
    """loan_percent_income > 1 (prêt supérieur au revenu annuel) → ValidationError."""
    schema = PredictionInputSchema()
    payload = {**VALID_PAYLOAD, "loan_percent_income": 1.5}
    with pytest.raises(ValidationError):
        schema.load(payload)
