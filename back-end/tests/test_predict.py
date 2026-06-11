# =============================================================================
# Fichier : back-end/tests/test_predict.py
# Rôle    : Tester les seuils de classification métier de _classify, valeurs
#           limites incluses (5 tests).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Tests unitaires pour app.predict._classify (seuils de classification)."""
import pytest

from app.predict import _classify


def test_classify_safe():
    """Proba < 0.3 → Safe, Accepté totalement."""
    risk, decision = _classify(0.2)
    assert risk == "Safe"
    assert decision == "Accepté totalement"


def test_classify_moyennement():
    """Proba 0.3 à 0.6 → Moyennement à risque, Accepté partiellement."""
    risk, decision = _classify(0.5)
    assert risk == "Moyennement à risque"
    assert decision == "Accepté partiellement"


def test_classify_risque():
    """Proba > 0.6 → À risque, Refusé."""
    risk, decision = _classify(0.7)
    assert risk == "À risque"
    assert decision == "Refusé"


def test_classify_seuil_inferieur():
    """Proba = 0.3 → Moyennement (limite inclusive)."""
    risk, decision = _classify(0.3)
    assert risk == "Moyennement à risque"


def test_classify_seuil_superieur():
    """Proba = 0.6 → À risque (limite exclusive)."""
    risk, decision = _classify(0.6)
    assert risk == "À risque"
