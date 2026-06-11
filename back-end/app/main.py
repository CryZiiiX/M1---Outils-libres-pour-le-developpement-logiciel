# =============================================================================
# Fichier : back-end/app/main.py
# Rôle    : Créer l'application Flask : CORS, enregistrement des routes et
#           handlers d'erreur globaux (module chargé par Gunicorn).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Point d'entrée de l'API Flask.

Crée l'application Flask, configure CORS, enregistre le blueprint des routes
et les handlers d'erreur globaux. Gunicorn charge ce module via app.main:app.

I/O : Application WSGI exposée via `app`. Les tables SQLAlchemy sont créées
au premier import (create_all). CORS ouvert (origins="*") pour le dev local
et le front-end sur un autre port.
"""
from flask import Flask, jsonify
from flask_cors import CORS

from .database import engine, Base
from .routes import router

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app, origins="*", allow_headers="*", supports_credentials=True)

app.register_blueprint(router)


@app.errorhandler(404)
def not_found(error):
    """Retourne une réponse 404 pour les ressources introuvables.

    Returns:
        JSON {"detail": str}, status 404.
    """
    return jsonify({"detail": error.description or "Ressource introuvable"}), 404


@app.errorhandler(400)
def bad_request(error):
    """Retourne une réponse 400 pour les requêtes invalides.

    Returns:
        JSON {"detail": str}, status 400.
    """
    return jsonify({"detail": error.description or "Requête invalide"}), 400


@app.errorhandler(500)
def internal_error(error):
    """Retourne une réponse 500 pour les erreurs internes du serveur.

    Returns:
        JSON {"detail": str}, status 500.
    """
    return jsonify({"detail": "Erreur interne du serveur"}), 500
