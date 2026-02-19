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
    """Contexte pour obtenir une session DB et la fermer automatiquement.

    Usage : `with get_db() as db: ...`. La session est fermée en sortie
    du bloc même en cas d'exception. Ne pas réutiliser la session après
    le bloc.

    Yields:
        Session SQLAlchemy. Fermeture garantie en sortie du bloc.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
