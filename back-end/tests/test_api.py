# =============================================================================
# Fichier : back-end/tests/test_api.py
# Rôle    : Tester les endpoints REST de bout en bout : codes 200/201/400/404,
#           persistance et bornes de validation (7 tests d'intégration).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Tests d'intégration API Flask."""
import pytest


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
    "model_choice": "both",
}


def test_health(client):
    """GET /health → 200, status ok."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_predict_valid(client):
    """POST /predict avec payload valide → 201, réponse avec lr, dt, id."""
    r = client.post(
        "/predict",
        json=VALID_PAYLOAD,
        content_type="application/json",
    )
    assert r.status_code == 201
    data = r.get_json()
    assert "id" in data
    assert "lr" in data
    assert "dt" in data
    assert data["lr"] is not None
    assert data["dt"] is not None
    assert "probability" in data["lr"]
    assert "risk_level" in data["lr"]


def test_predict_invalid(client):
    """POST /predict avec payload invalide → 400."""
    r = client.post(
        "/predict",
        json={"person_age": 17},
        content_type="application/json",
    )
    assert r.status_code == 400
    data = r.get_json()
    assert "detail" in data


def test_predict_loan_amnt_too_large(client):
    """POST /predict avec loan_amnt géant → 400 propre (et non un 500)."""
    r = client.post(
        "/predict",
        json={**VALID_PAYLOAD, "loan_amnt": 3_000_000_000},
        content_type="application/json",
    )
    assert r.status_code == 400
    data = r.get_json()
    assert "detail" in data


def test_predictions_list(client):
    """GET /predictions → 200, liste (éventuellement vide)."""
    r = client.get("/predictions")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)


def test_predictions_get_not_found(client):
    """GET /predictions/999999 → 404 si id inexistant."""
    r = client.get("/predictions/999999")
    assert r.status_code == 404
    data = r.get_json()
    assert "detail" in data


def test_predictions_get_existing(client):
    """GET /predictions/<id> → 200 après création d'une prédiction."""
    create_r = client.post("/predict", json=VALID_PAYLOAD, content_type="application/json")
    assert create_r.status_code == 201
    pred_id = create_r.get_json()["id"]
    r = client.get(f"/predictions/{pred_id}")
    assert r.status_code == 200
    data = r.get_json()
    assert data["id"] == pred_id
