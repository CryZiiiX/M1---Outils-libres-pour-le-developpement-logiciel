# =============================================================================
# Fichier : back-end/app/database.py
# Rôle    : Initialiser l'engine SQLAlchemy et fournir les sessions de base de
#           données utilisées par les routes.
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Configuration SQLAlchemy : engine, session, Base.

Crée l'engine, la SessionLocal et la Base déclarative. Pour SQLite,
check_same_thread=False est requis pour Flask (threading).
"""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import DATABASE_URL

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}  # SQLite requiert ce flag avec Flask

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db():
    """Fournit une session de base de données qui se ferme toute seule.

    S'utilise avec un bloc with : `with get_db() as db: ...`. L'intérêt du
    contextmanager est que la session est fermée dans tous les cas à la fin
    du bloc, même si une exception est levée au milieu - cela évite les
    fuites de connexions, une erreur facile à faire quand on gère les
    sessions à la main. La session ne doit pas être réutilisée après le bloc.

    Yields:
        Session SQLAlchemy prête à l'emploi.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
