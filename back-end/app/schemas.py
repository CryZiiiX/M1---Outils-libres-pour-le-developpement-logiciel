"""Schémas Marshmallow pour la validation des requêtes et réponses.

PredictionInputSchema : validation POST /predict.
PredictionRecordSchema : sérialisation des enregistrements pour GET.
"""
from marshmallow import Schema, fields, validate

HOME_OWNERSHIP_VALUES = ("RENT", "OWN", "MORTGAGE", "OTHER")
LOAN_INTENT_VALUES = (
    "PERSONAL", "EDUCATION", "MEDICAL", "VENTURE",
    "HOMEIMPROVEMENT", "DEBTCONSOLIDATION",
)
LOAN_GRADE_VALUES = ("A", "B", "C", "D", "E", "F", "G")
DEFAULT_ON_FILE_VALUES = ("N", "Y")
MODEL_CHOICE_VALUES = ("lr", "dt", "both")


class PredictionInputSchema(Schema):
    """Valide le payload POST /predict.

    Contraintes : âge 18-100, revenu 0-10M, loan_int_rate 0-30, etc.
    model_choice optionnel (lr|dt|both, défaut both). Clés catégorielles
    limitées aux valeurs définies (HOME_OWNERSHIP_VALUES, etc.).
    """
    person_age = fields.Integer(required=True, validate=validate.Range(min=18, max=100))
    person_income = fields.Integer(required=True, validate=validate.Range(min=0, max=10_000_000))
    person_home_ownership = fields.Str(required=True, validate=validate.OneOf(HOME_OWNERSHIP_VALUES))
    person_emp_length = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    loan_intent = fields.Str(required=True, validate=validate.OneOf(LOAN_INTENT_VALUES))
    loan_grade = fields.Str(required=True, validate=validate.OneOf(LOAN_GRADE_VALUES))
    loan_amnt = fields.Integer(required=True, validate=validate.Range(min=0))
    loan_int_rate = fields.Float(required=True, validate=validate.Range(min=0, max=30))
    loan_percent_income = fields.Float(required=True, validate=validate.Range(min=0))
    cb_person_default_on_file = fields.Str(required=True, validate=validate.OneOf(DEFAULT_ON_FILE_VALUES))
    cb_person_cred_hist_length = fields.Integer(required=True, validate=validate.Range(min=0, max=50))
    model_choice = fields.Str(load_default="both", validate=validate.OneOf(MODEL_CHOICE_VALUES))


class PredictionRecordSchema(Schema):
    """Sérialise un enregistrement Prediction pour les réponses GET.

    Inclut inputs + model_used + résultats LR/DT (probability, risk_level,
    credit_decision). Champs *_lr et *_dt nullables si modèle non utilisé.
    """
    id = fields.Integer()
    created_at = fields.DateTime()
    person_age = fields.Integer()
    person_income = fields.Integer()
    person_home_ownership = fields.Str()
    person_emp_length = fields.Float()
    loan_intent = fields.Str()
    loan_grade = fields.Str()
    loan_amnt = fields.Integer()
    loan_int_rate = fields.Float()
    loan_percent_income = fields.Float()
    cb_person_default_on_file = fields.Str()
    cb_person_cred_hist_length = fields.Integer()
    model_used = fields.Str()
    probability_lr = fields.Float(allow_none=True)
    risk_level_lr = fields.Str(allow_none=True)
    credit_decision_lr = fields.Str(allow_none=True)
    probability_dt = fields.Float(allow_none=True)
    risk_level_dt = fields.Str(allow_none=True)
    credit_decision_dt = fields.Str(allow_none=True)
