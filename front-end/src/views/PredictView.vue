<template>
  <div class="space-y-8">
    <PredictionForm :loading="loading" @submit="handleSubmit" />

    <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

    <!-- Résultats -->
    <div v-if="result" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <ResultCard v-if="result.lr" title="Régression Logistique" :result="result.lr" />
      <ResultCard v-if="result.dt" title="Arbre de Décision" :result="result.dt" />
    </div>
  </div>
</template>

<script setup>
/**
 * Vue principale : formulaire de prédiction + affichage résultats LR/DT.
 * Appelle postPredict sur submit, affiche ResultCard pour chaque modèle.
 */
import { ref } from 'vue'
import PredictionForm from '../components/PredictionForm.vue'
import ResultCard from '../components/ResultCard.vue'
import { postPredict } from '../api/client.js'


const loading = ref(false)
const result = ref(null)
const error = ref(null)


/**
 * Envoie le formulaire à l'API /predict et affiche les résultats LR/DT.
 * @param {Object} form - Données du formulaire (person_age, person_income, etc.)
 */
async function handleSubmit(form) {
  loading.value = true
  error.value = null
  result.value = null
  try {
    result.value = await postPredict(form)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
