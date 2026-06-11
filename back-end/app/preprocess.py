# =============================================================================
# Fichier : back-end/app/preprocess.py
# Rôle    : Encoder les variables d'une demande de crédit dans l'ordre attendu
#           par les modèles (mappings partagés avec l'entraînement).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Prétraitement des données pour la prédiction.

Encodage des variables catégorielles, aligné avec compare_with_sklearn._encode_dataframe.

Invariant : FEATURE_ORDER doit rester identique à l'ordre des colonnes utilisées
à l'entraînement (df.drop('loan_status') après encodage). Toute modification
doit être synchronisée avec _encode_dataframe dans compare_with_sklearn.py.
"""
import numpy as np

HOME_MAPPING = {'RENT': 0, 'OWN': 1, 'MORTGAGE': 2, 'OTHER': 3}
INTENT_MAPPING = {
    'PERSONAL': 0, 'EDUCATION': 1, 'MEDICAL': 2,
    'VENTURE': 3, 'HOMEIMPROVEMENT': 4, 'DEBTCONSOLIDATION': 5,
}
GRADE_MAPPING = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
DEFAULT_MAPPING = {'N': 0, 'Y': 1}

# Ordre des colonnes attendu par les modèles. Ne pas modifier sans sync compare_with_sklearn.
FEATURE_ORDER = [
    'person_age',
    'person_income',
    'person_home_ownership',
    'person_emp_length',
    'loan_intent',
    'loan_grade',
    'loan_amnt',
    'loan_int_rate',
    'loan_percent_income',
    'cb_person_default_on_file',
    'cb_person_cred_hist_length',
]


def encode_input(data: dict) -> np.ndarray:
    """Convertit les données reçues depuis l'API en vecteur numérique
    utilisable par les modèles de machine learning.

    Les quatre variables catégorielles (statut de propriété, objet du prêt,
    grade, antécédent de défaut) sont transformées en entiers via les mêmes
    dictionnaires de correspondance que ceux utilisés à l'entraînement, puis
    les 11 variables sont rangées dans l'ordre exact de FEATURE_ORDER. Cette
    étape est importante : un ordre différent des features donnerait une
    prédiction incohérente sans déclencher la moindre erreur.

    Args:
        data (dict): Données déjà validées par le schéma Marshmallow.

    Returns:
        numpy.ndarray: Tableau de forme (1, 11), prêt à être passé aux modèles.
    """
    encoded = {
        'person_age': data['person_age'],
        'person_income': data['person_income'],
        'person_home_ownership': HOME_MAPPING[data['person_home_ownership']],
        'person_emp_length': data['person_emp_length'],
        'loan_intent': INTENT_MAPPING[data['loan_intent']],
        'loan_grade': GRADE_MAPPING[data['loan_grade']],
        'loan_amnt': data['loan_amnt'],
        'loan_int_rate': data['loan_int_rate'],
        'loan_percent_income': data['loan_percent_income'],
        'cb_person_default_on_file': DEFAULT_MAPPING[data['cb_person_default_on_file']],
        'cb_person_cred_hist_length': data['cb_person_cred_hist_length'],
    }

    features = [encoded[f] for f in FEATURE_ORDER]
    return np.array([features], dtype=float)
