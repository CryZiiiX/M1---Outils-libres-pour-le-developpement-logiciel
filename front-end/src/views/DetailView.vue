<!--
=============================================================================
Fichier : front-end/src/views/DetailView.vue
Rôle    : Afficher le détail complet d'une prédiction sélectionnée
(données saisies et résultats des deux modèles).
Projet  : Prédiction du risque de crédit bancaire
UE      : Outils libres pour le développement logiciel
Auteur  : Maxime BRONNY - 19009314
Version : V1
Cadre   : Master 1 Big Data - Université Paris 8
=============================================================================
-->
<template>
  <div class="space-y-6">
    <router-link to="/history" class="text-indigo-600 hover:underline text-sm">&larr; Retour à l'historique</router-link>

    <p v-if="loading" class="text-gray-500 text-sm">Chargement...</p>
    <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

    <template v-if="record">
      <h2 class="text-xl font-bold text-gray-800">Prédiction #{{ record.id }}</h2>
      <p class="text-sm text-gray-500">{{ new Date(record.created_at).toLocaleString('fr-FR') }}</p>

      <!-- Entrées -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="font-semibold text-gray-700 mb-3">Données saisies</h3>
        <dl class="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-2 text-sm">
          <div><dt class="text-gray-500">Âge</dt><dd class="font-medium">{{ record.person_age }}</dd></div>
          <div><dt class="text-gray-500">Revenu</dt><dd class="font-medium">${{ record.person_income.toLocaleString() }}</dd></div>
          <div><dt class="text-gray-500">Propriété</dt><dd class="font-medium">{{ record.person_home_ownership }}</dd></div>
          <div><dt class="text-gray-500">Années d'emploi</dt><dd class="font-medium">{{ record.person_emp_length }}</dd></div>
          <div><dt class="text-gray-500">Objet du prêt</dt><dd class="font-medium">{{ record.loan_intent }}</dd></div>
          <div><dt class="text-gray-500">Grade</dt><dd class="font-medium">{{ record.loan_grade }}</dd></div>
          <div><dt class="text-gray-500">Montant</dt><dd class="font-medium">${{ record.loan_amnt.toLocaleString() }}</dd></div>
          <div><dt class="text-gray-500">Taux d'intérêt</dt><dd class="font-medium">{{ record.loan_int_rate }}%</dd></div>
          <div><dt class="text-gray-500">Ratio prêt/revenu</dt><dd class="font-medium">{{ record.loan_percent_income }}</dd></div>
          <div><dt class="text-gray-500">Défaut passé</dt><dd class="font-medium">{{ record.cb_person_default_on_file }}</dd></div>
          <div><dt class="text-gray-500">Historique crédit</dt><dd class="font-medium">{{ record.cb_person_cred_hist_length }} ans</dd></div>
          <div><dt class="text-gray-500">Modèle</dt><dd class="font-medium uppercase">{{ record.model_used }}</dd></div>
        </dl>
      </div>

      <!-- Résultats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ResultCard
          v-if="record.probability_lr != null"
          title="Régression Logistique"
          :result="{ probability: record.probability_lr, risk_level: record.risk_level_lr, credit_decision: record.credit_decision_lr }"
        />
        <ResultCard
          v-if="record.probability_dt != null"
          title="Arbre de Décision"
          :result="{ probability: record.probability_dt, risk_level: record.risk_level_dt, credit_decision: record.credit_decision_dt }"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
/**
 * Vue détail : prédiction par ID via getPrediction(route.params.id).
 * Affiche inputs + résultats LR/DT (ResultCard).
 */
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ResultCard from '../components/ResultCard.vue'
import { getPrediction } from '../api/client.js'


const route = useRoute()
const record = ref(null)
const loading = ref(true)
const error = ref(null)


onMounted(async () => {
  try {
    record.value = await getPrediction(route.params.id)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
