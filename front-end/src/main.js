/* =============================================================================
 * Fichier : front-end/src/main.js
 * Rôle    : Initialiser l'application Vue 3 : création de l'app, enregistrement
 *           du routeur et montage sur la page.
 * Projet  : Prédiction du risque de crédit bancaire
 * UE      : Outils libres pour le développement logiciel
 * Auteur  : Maxime BRONNY - 19009314
 * Version : V1
 * Cadre   : Master 1 Big Data - Université Paris 8
 * ============================================================================= */
/** Point d'entrée Vue : crée l'app, enregistre le router, monte sur #app. */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'


createApp(App).use(router).mount('#app')
