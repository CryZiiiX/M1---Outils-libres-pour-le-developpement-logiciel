<!--
=============================================================================
Fichier : front-end/src/views/HistoryView.vue
Rôle    : Afficher l'historique des prédictions enregistrées en base.
Projet  : Prédiction du risque de crédit bancaire
UE      : Outils libres pour le développement logiciel
Auteur  : Maxime BRONNY - 19009314
Version : V1
Cadre   : Master 1 Big Data - Université Paris 8
=============================================================================
-->
<template>
  <div class="space-y-4">
    <h2 class="text-xl font-bold text-gray-800">Historique des prédictions</h2>

    <p v-if="loading" class="text-gray-500 text-sm">Chargement...</p>
    <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

    <div v-if="records.length" class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 text-left">#</th>
            <th class="px-4 py-2 text-left">Date</th>
            <th class="px-4 py-2 text-left">Modèle</th>
            <th class="px-4 py-2 text-left">Montant</th>
            <th class="px-4 py-2 text-left">Proba LR</th>
            <th class="px-4 py-2 text-left">Proba DT</th>
            <th class="px-4 py-2 text-left">Décision</th>
            <th class="px-4 py-2"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in records" :key="r.id" class="border-t hover:bg-gray-50">
            <td class="px-4 py-2">{{ r.id }}</td>
            <td class="px-4 py-2">{{ new Date(r.created_at).toLocaleString('fr-FR') }}</td>
            <td class="px-4 py-2 uppercase font-medium">{{ r.model_used }}</td>
            <td class="px-4 py-2">${{ r.loan_amnt.toLocaleString() }}</td>
            <td class="px-4 py-2">{{ r.probability_lr != null ? (r.probability_lr * 100).toFixed(1) + '%' : '-' }}</td>
            <td class="px-4 py-2">{{ r.probability_dt != null ? (r.probability_dt * 100).toFixed(1) + '%' : '-' }}</td>
            <td class="px-4 py-2">
              <span v-if="r.credit_decision_lr" class="mr-1">{{ r.credit_decision_lr }}</span>
              <span v-if="r.credit_decision_lr && r.credit_decision_dt"> / </span>
              <span v-if="r.credit_decision_dt">{{ r.credit_decision_dt }}</span>
            </td>
            <td class="px-4 py-2">
              <router-link :to="`/history/${r.id}`" class="text-indigo-600 hover:underline text-sm">Détail</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else-if="!loading" class="text-gray-400 text-sm">Aucune prédiction enregistrée.</p>
  </div>
</template>

<script setup>
/**
 * Vue historique : liste des prédictions via getPredictions.
 * Charge au montage, affiche tableau avec lien vers détail.
 */
import { ref, onMounted } from 'vue'
import { getPredictions } from '../api/client.js'


const records = ref([])
const loading = ref(true)
const error = ref(null)


onMounted(async () => {
  try {
    records.value = await getPredictions()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
