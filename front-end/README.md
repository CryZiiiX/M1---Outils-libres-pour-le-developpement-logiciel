# Front-end - Prédiction du risque de crédit

Interface web du projet (Vue 3 + Vite + Tailwind CSS) : formulaire de
demande de prédiction, affichage des résultats des deux modèles et
historique des prédictions.

## Développement local

```bash
npm install
npm run dev      # http://localhost:5173 (API attendue sur :8000)
```

L'URL de l'API est configurable via la variable d'environnement
`VITE_API_URL` (par défaut `http://localhost:8000`).

## Via Docker

Le service `web` de `../docker-compose.yml` construit et lance ce front-end
automatiquement : voir `make docker-up` à la racine du projet.
