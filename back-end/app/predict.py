"""Chargement des modèles et logique de prédiction.

Charge au démarrage les modèles joblib (LR, scaler, DT) et expose predict_lr
et predict_dt. Les seuils de classification sont définis dans _classify.

Invariant : FEATURE_ORDER (preprocess) doit correspondre à l'ordre des
colonnes utilisées à l'entraînement (compare_with_sklearn._preprocess_dataframe).
"""
import joblib
import pandas as pd

from .config import LR_MODEL_PATH, SCALER_PATH, DT_MODEL_PATH
from .preprocess import encode_input, FEATURE_ORDER

lr_model = joblib.load(LR_MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
dt_model = joblib.load(DT_MODEL_PATH)


def _classify(probability: float) -> tuple[str, str]:
    """Détermine le niveau de risque et la décision selon la probabilité de défaut.

    Seuils métier : < 30 % = Safe, 30-60 % = Moyennement à risque, > 60 % = Refusé.

    Args:
        probability: Probabilité de défaut (0-1) prédite par le modèle.

    Returns:
        Tuple (risk_level, credit_decision).
    """
    if probability < 0.3:  # Politique conservatrice : < 30 % défaut = Safe
        return "Safe", "Accepté totalement"
    elif probability < 0.6:
        return "Moyennement à risque", "Accepté partiellement"
    else:
        return "À risque", "Refusé"


def predict_lr(data: dict) -> dict:
    """Prédiction avec la régression logistique.

    Applique encode_input puis le scaler (StandardScaler) avant prédiction.
    Le modèle LR nécessite une normalisation des features.

    Args:
        data: Dictionnaire des champs du formulaire (clés alignées avec preprocess).

    Returns:
        Dict avec probability, risk_level, credit_decision.

    Raises:
        FileNotFoundError: Si models/*.joblib absents (exécuter make train).
    """
    features = encode_input(data)
    features_df = pd.DataFrame(features, columns=FEATURE_ORDER)
    features_scaled = scaler.transform(features_df)
    probability = float(lr_model.predict_proba(features_scaled)[0, 1])
    risk_level, credit_decision = _classify(probability)

    return {
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "credit_decision": credit_decision,
    }


def predict_dt(data: dict) -> dict:
    """Prédiction avec l'arbre de décision.

    Applique encode_input uniquement. L'arbre de décision n'utilise pas
    le scaler (features brutes). DataFrame avec noms de colonnes pour
    éviter les warnings sklearn.

    Args:
        data: Dictionnaire des champs du formulaire.

    Returns:
        Dict avec probability, risk_level, credit_decision.

    Raises:
        FileNotFoundError: Si models/*.joblib absents (exécuter make train).
    """
    features = encode_input(data)
    features_df = pd.DataFrame(features, columns=FEATURE_ORDER)
    probability = float(dt_model.predict_proba(features_df)[0, 1])
    risk_level, credit_decision = _classify(probability)

    return {
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "credit_decision": credit_decision,
    }
