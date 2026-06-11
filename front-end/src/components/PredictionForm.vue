<!--
=============================================================================
Fichier : front-end/src/components/PredictionForm.vue
Rôle    : Saisir les 11 caractéristiques d'une demande de crédit, avec calcul
automatique du ratio prêt/revenu.
Projet  : Prédiction du risque de crédit bancaire
UE      : Outils libres pour le développement logiciel
Auteur  : Maxime BRONNY - 19009314
Version : V1
Cadre   : Master 1 Big Data - Université Paris 8
=============================================================================
-->
<template>
  <form @submit.prevent="$emit('submit', form)" class="bg-white rounded-lg shadow p-6 space-y-6">
    <h2 class="text-lg font-semibold text-gray-800">Informations du demandeur</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- person_age -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Âge</label>
        <input v-model.number="form.person_age" type="number" min="18" max="100" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- person_income -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Revenu annuel ($)</label>
        <input v-model.number="form.person_income" type="number" min="0" max="10000000" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- person_home_ownership -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Propriété</label>
        <select v-model="form.person_home_ownership" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500">
          <option value="RENT">Location (RENT)</option>
          <option value="OWN">Propriétaire (OWN)</option>
          <option value="MORTGAGE">Hypothèque (MORTGAGE)</option>
          <option value="OTHER">Autre (OTHER)</option>
        </select>
      </div>

      <!-- person_emp_length -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Années d'emploi</label>
        <input v-model.number="form.person_emp_length" type="number" min="0" max="100" step="0.1" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- loan_intent -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Objet du prêt</label>
        <select v-model="form.loan_intent" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500">
          <option value="PERSONAL">Personnel</option>
          <option value="EDUCATION">Éducation</option>
          <option value="MEDICAL">Médical</option>
          <option value="VENTURE">Investissement</option>
          <option value="HOMEIMPROVEMENT">Rénovation</option>
          <option value="DEBTCONSOLIDATION">Consolidation de dettes</option>
        </select>
      </div>

      <!-- loan_grade -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Grade du prêt</label>
        <select v-model="form.loan_grade" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500">
          <option v-for="g in ['A','B','C','D','E','F','G']" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>

      <!-- loan_amnt -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Montant du prêt ($)</label>
        <input v-model.number="form.loan_amnt" type="number" min="0" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- loan_int_rate -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Taux d'intérêt (%)</label>
        <input v-model.number="form.loan_int_rate" type="number" min="0" max="30" step="0.01" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- loan_percent_income -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Ratio prêt/revenu</label>
        <input v-model.number="form.loan_percent_income" type="number" min="0" step="0.01" required readonly
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500 bg-gray-50" />
      </div>

      <!-- cb_person_default_on_file -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Antécédent de défaut</label>
        <select v-model="form.cb_person_default_on_file" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500">
          <option value="N">Non</option>
          <option value="Y">Oui</option>
        </select>
      </div>

      <!-- cb_person_cred_hist_length -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Historique crédit (années)</label>
        <input v-model.number="form.cb_person_cred_hist_length" type="number" min="0" max="50" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500" />
      </div>

      <!-- model_choice -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Modèle</label>
        <select v-model="form.model_choice" required
          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-indigo-500 focus:border-indigo-500">
          <option value="lr">Régression logistique</option>
          <option value="dt">Arbre de décision</option>
          <option value="both">Les deux</option>
        </select>
      </div>
    </div>

    <button type="submit" :disabled="loading"
      class="w-full md:w-auto px-6 py-2 bg-indigo-600 text-white rounded font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed">
      {{ loading ? 'Analyse en cours...' : 'Prédire' }}
    </button>
  </form>
</template>

<script setup>
/**
 * Formulaire de prédiction : 11 champs alignés sur l'API POST /predict.
 * Emits 'submit' avec l'objet form. loan_percent_income calculé automatiquement.
 */
import { reactive, watch } from 'vue'


defineProps({ loading: Boolean })
defineEmits(['submit'])


const form = reactive({
  person_age: 30,
  person_income: 50000,
  person_home_ownership: 'RENT',
  person_emp_length: 5,
  loan_intent: 'PERSONAL',
  loan_grade: 'B',
  loan_amnt: 10000,
  loan_int_rate: 10,
  loan_percent_income: 0.2,
  cb_person_default_on_file: 'N',
  cb_person_cred_hist_length: 5,
  model_choice: 'both',
})


/** Calcule loan_percent_income = loan_amnt / person_income (ratio prêt/revenu). */
watch(
  () => [form.person_income, form.loan_amnt],
  ([income, amnt]) => {
    form.loan_percent_income = income > 0 ? amnt / income : 0
  },
  { immediate: true }
)
</script>
