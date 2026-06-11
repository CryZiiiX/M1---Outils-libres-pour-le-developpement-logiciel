# =============================================================================
# Fichier : back-end/app/predict.py
# Rôle    : Charger les modèles joblib et produire les prédictions de risque
#           (probabilité, niveau de risque, décision selon les seuils métier).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Chargement des modèles et logique de prédiction.

Charge au démarrage les modèles joblib (LR, scaler, DT) et expose predict_lr
et predict_dt. Les seuils de classification sont définis dans _classify.

Invariant : FEATURE_ORDER (preprocess) doit correspondre à l'ordre des
colonnes utilisées à l'entraînement (compare_with_sklearn._encode_dataframe).
"""
import joblib
import pandas as pd

from .config import LR_MODEL_PATH, SCALER_PATH, DT_MODEL_PATH
from .preprocess import encode_input, FEATURE_ORDER

try:
    lr_model = joblib.load(LR_MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    dt_model = joblib.load(DT_MODEL_PATH)
except FileNotFoundError as exc:
    # Message explicite plutôt qu'une stack trace confuse au démarrage :
    # les modèles doivent être entraînés avant de lancer l'API.
    raise RuntimeError(
        "Modèles introuvables dans back-end/models/ "
        f"(fichier manquant : {exc.filename}). "
        "Lancez d'abord « make train » à la racine du projet "
        "(ou « make docker-up » qui enchaîne entraînement et déploiement), "
        "puis redémarrez l'API."
    ) from exc


def _classify(probability: float) -> tuple[str, str]:
    """Traduit une probabilité de défaut en niveau de risque et en décision
    de crédit compréhensibles par l'utilisateur.

    Les modèles renvoient seulement une probabilité entre 0 et 1 : ce sont
    les seuils métier qui la transforment en décision. En dessous de 30 %
    de risque, le prêt est accepté totalement ; entre 30 et 60 %, il est
    accepté partiellement (profil moyennement risqué) ; au-delà de 60 %,
    il est refusé. Ces seuils sont volontairement prudents et pourraient
    être ajustés selon la politique de l'établissement prêteur.

    Args:
        probability (float): Probabilité de défaut prédite (entre 0 et 1).

    Returns:
        tuple: (niveau de risque, décision de crédit), deux chaînes affichées
        telles quelles dans l'interface.
    """
    if probability < 0.3:  # Politique conservatrice : < 30 % défaut = Safe
        return "Safe", "Accepté totalement"
    elif probability < 0.6:
        return "Moyennement à risque", "Accepté partiellement"
    else:
        return "À risque", "Refusé"


def predict_lr(data: dict) -> dict:
    """Prédit le risque de défaut avec la régression logistique.

    Les données sont d'abord encodées en vecteur numérique, puis normalisées
    avec le StandardScaler appris à l'entraînement : la régression logistique
    a été entraînée sur des features centrées-réduites, il faut donc appliquer
    exactement la même transformation ici, sinon la prédiction n'aurait aucun
    sens. Le passage par un DataFrame avec les noms de colonnes évite les
    avertissements de scikit-learn sur les features sans nom.

    Args:
        data (dict): Champs du formulaire validés (clés alignées avec preprocess).

    Returns:
        dict: probability (arrondie à 4 décimales), risk_level et
        credit_decision issus des seuils métier.
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
    """Prédit le risque de défaut avec l'arbre de décision.

    Contrairement à la régression logistique, l'arbre n'a pas besoin de
    normalisation : ses décisions reposent sur des comparaisons à des seuils
    bruts (par exemple « revenu < 35 000 »), qui ne sont pas affectées par
    l'échelle des variables. On encode donc les données et on prédit
    directement, sans passer par le scaler.

    Args:
        data (dict): Champs du formulaire validés.

    Returns:
        dict: probability (arrondie à 4 décimales), risk_level et
        credit_decision issus des seuils métier.
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
