"""Endpoints de l'API Flask.

Expose les routes POST /predict, GET /predictions, GET /predictions/<id> et GET /health.
Validation des entrées via Marshmallow, persistance en base via SQLAlchemy.
"""
from flask import Blueprint, request, jsonify, abort

from .database import get_db
from .models import Prediction
from .schemas import (
    PredictionInputSchema,
    PredictionRecordSchema,
)
from .predict import predict_lr, predict_dt
from marshmallow import ValidationError

router = Blueprint("api", __name__)

input_schema = PredictionInputSchema()
record_schema = PredictionRecordSchema()


@router.get("/health")
def health():
    """Vérifie que l'API est opérationnelle."""
    return jsonify({"status": "ok"})


@router.post("/predict")
def create_prediction():
    """Lance une prédiction et l'enregistre en base.

    Valide le payload, appelle predict_lr et/ou predict_dt selon model_choice,
    persiste le résultat et retourne la réponse JSON.

    Args:
        Body JSON : 11 champs requis (person_age, person_income, ...) + model_choice optionnel.

    Returns:
        JSON : id, created_at, model_used, lr, dt. Status 201.

    Raises:
        ValidationError (400): Payload invalide (champs manquants, hors bornes).
    """
    try:
        payload = input_schema.load(request.get_json(silent=True) or {})
    except ValidationError as e:
        return jsonify({"detail": str(e.messages)}), 400

    data = {
        "person_age": payload["person_age"],
        "person_income": payload["person_income"],
        "person_home_ownership": payload["person_home_ownership"],
        "person_emp_length": payload["person_emp_length"],
        "loan_intent": payload["loan_intent"],
        "loan_grade": payload["loan_grade"],
        "loan_amnt": payload["loan_amnt"],
        "loan_int_rate": payload["loan_int_rate"],
        "loan_percent_income": payload["loan_percent_income"],
        "cb_person_default_on_file": payload["cb_person_default_on_file"],
        "cb_person_cred_hist_length": payload["cb_person_cred_hist_length"],
    }

    lr_result = None
    dt_result = None
    model_choice = payload.get("model_choice", "both")

    if model_choice in ("lr", "both"):
        lr_result = predict_lr(data)

    if model_choice in ("dt", "both"):
        dt_result = predict_dt(data)

    with get_db() as db:
        record = Prediction(
            **data,
            model_used=model_choice,
            probability_lr=lr_result["probability"] if lr_result else None,
            risk_level_lr=lr_result["risk_level"] if lr_result else None,
            credit_decision_lr=lr_result["credit_decision"] if lr_result else None,
            probability_dt=dt_result["probability"] if dt_result else None,
            risk_level_dt=dt_result["risk_level"] if dt_result else None,
            credit_decision_dt=dt_result["credit_decision"] if dt_result else None,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        response_data = {
            "id": record.id,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "model_used": record.model_used,
            "lr": lr_result,
            "dt": dt_result,
        }
        return jsonify(response_data), 201


@router.get("/predictions")
def list_predictions():
    """Renvoie l'historique des prédictions (plus récentes d'abord).

    Args:
        limit (query): Nombre max de résultats (1-200, défaut 50).

    Returns:
        Liste JSON des prédictions (schema PredictionRecordSchema).
    """
    limit = request.args.get("limit", 50, type=int)
    if limit < 1 or limit > 200:
        limit = 50

    with get_db() as db:
        records = (
            db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .limit(limit)
            .all()
        )
        return jsonify(record_schema.dump(records, many=True))


@router.get("/predictions/<int:prediction_id>")
def get_prediction(prediction_id):
    """Renvoie le détail d'une prédiction par son ID.

    Args:
        prediction_id: Identifiant de la prédiction.

    Returns:
        Objet JSON de la prédiction. 404 si introuvable.
    """
    with get_db() as db:
        record = db.query(Prediction).filter(Prediction.id == prediction_id).first()
        if not record:
            abort(404, description="Prédiction introuvable")
        return jsonify(record_schema.dump(record))
