# =============================================================================
# Fichier : back-end/tests/test_imputation.py
# Rôle    : Vérifier l'absence de fuite de données dans l'imputation : les
#           statistiques proviennent du train uniquement (3 tests).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Tests anti-fuite de données pour l'imputation du pipeline ML.

Vérifie que les statistiques d'imputation sont apprises sur le train set
uniquement et que les valeurs du test set ne les influencent jamais
(scripts/compare_with_sklearn.py : compute_imputation_values, apply_imputation).
"""
import sys
from pathlib import Path

import pandas as pd

# scripts/ n'est pas un package : on l'ajoute au path pour importer le module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from compare_with_sklearn import (  # noqa: E402
    _encode_dataframe,
    apply_imputation,
    compute_imputation_values,
)


def test_imputation_values_computed_on_train_only():
    """Les moyennes d'imputation proviennent du train, pas du test."""
    train = pd.DataFrame({"loan_int_rate": [10.0, 20.0], "person_age": [30, 40]})
    impute_values = compute_imputation_values(train)
    assert impute_values["loan_int_rate"] == 15.0
    assert impute_values["person_age"] == 35.0


def test_test_set_nan_filled_with_train_mean():
    """Un NaN du test set est rempli avec la moyenne du TRAIN.

    Le test set contient des valeurs extrêmes (99.0) : si l'imputation
    fuyait, la valeur remplie serait influencée par ces 99.0.
    """
    train = pd.DataFrame({"loan_int_rate": [10.0, 20.0]})
    test = pd.DataFrame({"loan_int_rate": [99.0, None, 99.0]})
    impute_values = compute_imputation_values(train)
    test_filled = apply_imputation(test, impute_values)
    # Moyenne du train (15.0), surtout pas du test (99.0) ni du mélange
    assert test_filled["loan_int_rate"].iloc[1] == 15.0
    assert not test_filled["loan_int_rate"].isna().any()


def test_encode_preserves_column_order():
    """L'encodage conserve l'ordre des colonnes (invariant FEATURE_ORDER)."""
    from app.preprocess import FEATURE_ORDER

    df = pd.DataFrame([{
        "person_age": 30,
        "person_income": 50000,
        "person_home_ownership": "RENT",
        "person_emp_length": 5.0,
        "loan_intent": "PERSONAL",
        "loan_grade": "B",
        "loan_amnt": 10000,
        "loan_int_rate": 10.0,
        "loan_percent_income": 0.2,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 5,
    }])
    encoded = _encode_dataframe(df)
    assert list(encoded.columns) == FEATURE_ORDER
    # Les mappings catégoriels sont bien ceux partagés avec l'API
    assert encoded["person_home_ownership"].iloc[0] == 0  # RENT -> 0
    assert encoded["loan_grade"].iloc[0] == 2             # B -> 2
