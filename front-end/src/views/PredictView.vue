<!--
=============================================================================
Fichier : front-end/src/views/PredictView.vue
Rôle    : Afficher le formulaire de prédiction et présenter les résultats
retournés par l'API pour chaque modèle.
Projet  : Prédiction du risque de crédit bancaire
UE      : Outils libres pour le développement logiciel
Auteur  : Maxime BRONNY - 19009314
Version : V1
Cadre   : Master 1 Big Data - Université Paris 8
=============================================================================
-->
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
 * Soumet le formulaire de prédiction à l'API.
 *
 * La fonction passe la vue en état de chargement (le bouton est désactivé
 * pendant la requête), appelle l'API /predict puis affiche les résultats
 * des deux modèles. En cas d'erreur (payload refusé en 400 ou API
 * injoignable), le message renvoyé par le client API est affiché à
 * l'utilisateur à la place des résultats.
 *
 * @param {Object} form - Données saisies dans le formulaire (11 champs + model_choice).
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
