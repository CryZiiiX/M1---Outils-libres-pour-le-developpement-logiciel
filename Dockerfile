# =============================================================================
# Fichier : Dockerfile
# Rôle    : Construire l'image de reproduction du pipeline ML complet
#           (exécute make all dans un environnement isolé).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================

FROM python:3.11-slim

# Installer make pour exécuter le Makefile
RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier requirements.txt en premier pour optimiser le cache Docker
COPY back-end/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Commande par défaut : exécuter le pipeline Python complet
CMD ["make", "all"]
