/* =============================================================================
 * Fichier : front-end/src/router/index.js
 * Rôle    : Définir les routes du front-end : formulaire de prédiction,
 *           historique et détail d'une prédiction.
 * Projet  : Prédiction du risque de crédit bancaire
 * UE      : Outils libres pour le développement logiciel
 * Auteur  : Maxime BRONNY - 19009314
 * Version : V1
 * Cadre   : Master 1 Big Data - Université Paris 8
 * ============================================================================= */
/**
 * Configuration des routes Vue Router.
 *
 * Routes : / (prédiction), /history (liste), /history/:id (détail).
 * Pas de garde d'authentification.
 */
import { createRouter, createWebHistory } from 'vue-router'
import PredictView from '../views/PredictView.vue'
import HistoryView from '../views/HistoryView.vue'
import DetailView from '../views/DetailView.vue'


const routes = [
  { path: '/', name: 'predict', component: PredictView },
  { path: '/history', name: 'history', component: HistoryView },
  { path: '/history/:id', name: 'detail', component: DetailView },
]


export default createRouter({
  history: createWebHistory(),
  routes,
})
