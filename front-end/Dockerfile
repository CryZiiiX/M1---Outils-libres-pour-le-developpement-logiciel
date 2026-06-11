# =============================================================================
# Fichier : front-end/Dockerfile
# Rôle    : Construire l'image Docker du front-end Vue (serveur de
#           développement Vite).
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
# Image front-end Vue : Vite dev server
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Port exposé : 5173 (Vite)
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
