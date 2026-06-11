# =============================================================================
# Fichier : back-end/tests/conftest.py
# Rôle    : Fournir les fixtures pytest : base SQLite en mémoire et client de
#           test Flask (isolation des tests).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Fixtures pytest pour les tests API.

DATABASE_URL=sqlite:///:memory: défini avant import pour isoler les tests
(sans fichier, sans PostgreSQL). client : test_client Flask en mode TESTING.
"""
import os

import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.main import app


@pytest.fixture
def client():
    """Fournit un client HTTP de test pour appeler l'API sans serveur réel.

    Le test_client de Flask simule des requêtes HTTP directement en mémoire,
    sans ouvrir de socket réseau. Combiné à la base SQLite en mémoire
    (définie avant l'import de l'application, sinon l'engine serait déjà
    créé sur la mauvaise base), chaque session de tests est totalement
    isolée : pas de PostgreSQL requis, pas de fichier créé, pas d'état
    persistant entre deux lancements.

    Yields:
        FlaskClient: Client de test utilisé par les tests d'API.
    """
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
