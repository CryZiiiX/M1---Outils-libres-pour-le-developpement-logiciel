/* =============================================================================
 * Fichier : front-end/vite.config.js
 * Rôle    : Configurer Vite : plugins Vue et Tailwind, écoute réseau 0.0.0.0
 *           pour l'accès depuis l'hôte (Docker).
 * Projet  : Prédiction du risque de crédit bancaire
 * UE      : Outils libres pour le développement logiciel
 * Auteur  : Maxime BRONNY - 19009314
 * Version : V1
 * Cadre   : Master 1 Big Data - Université Paris 8
 * ============================================================================= */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
})
