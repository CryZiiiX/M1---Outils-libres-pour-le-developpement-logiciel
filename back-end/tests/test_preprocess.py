"""Tests unitaires pour app.preprocess.encode_input."""
import numpy as np
import pytest

from app.preprocess import encode_input, FEATURE_ORDER


def test_encode_input_shape():
    """encode_input retourne un array de shape (1, 11)."""
    data = {
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
    result = encode_input(data)
    assert result.shape == (1, 11)


def test_encode_input_categorical_mappings():
    """Encodage correct : RENT→0, A→1, N→0."""
    data = {
        "person_age": 25,
        "person_income": 40000,
        "person_home_ownership": "RENT",
        "person_emp_length": 3,
        "loan_intent": "EDUCATION",
        "loan_grade": "A",
        "loan_amnt": 5000,
        "loan_int_rate": 8,
        "loan_percent_income": 0.125,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 2,
    }
    result = encode_input(data)
    arr = result[0]
    idx_home = FEATURE_ORDER.index("person_home_ownership")
    idx_grade = FEATURE_ORDER.index("loan_grade")
    idx_default = FEATURE_ORDER.index("cb_person_default_on_file")
    assert arr[idx_home] == 0  # RENT
    assert arr[idx_grade] == 1  # A
    assert arr[idx_default] == 0  # N


def test_encode_input_feature_order():
    """Les features sont dans l'ordre FEATURE_ORDER."""
    data = {
        "person_age": 30,
        "person_income": 50000,
        "person_home_ownership": "OWN",
        "person_emp_length": 5,
        "loan_intent": "PERSONAL",
        "loan_grade": "G",
        "loan_amnt": 10000,
        "loan_int_rate": 10,
        "loan_percent_income": 0.2,
        "cb_person_default_on_file": "Y",
        "cb_person_cred_hist_length": 5,
    }
    result = encode_input(data)
    assert result[0, 0] == 30  # person_age
    assert result[0, 1] == 50000  # person_income
    assert result[0, 2] == 1  # OWN
    assert result[0, 10] == 5  # cb_person_cred_hist_length
