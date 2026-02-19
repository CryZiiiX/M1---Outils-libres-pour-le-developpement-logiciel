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
