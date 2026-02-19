# ============================================================================
# Dockerfile - Prédiction du Risque de Crédit Bancaire (Python)
# ============================================================================
# Image Docker pour la reproductibilité du projet Python.
# ============================================================================

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
