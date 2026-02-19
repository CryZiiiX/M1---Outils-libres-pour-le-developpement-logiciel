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
    """Client Flask pour les tests API. Isolé en mémoire (SQLite)."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c
