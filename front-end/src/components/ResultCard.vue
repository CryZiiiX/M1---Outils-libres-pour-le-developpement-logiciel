<template>
  <div class="bg-white rounded-lg shadow p-6 space-y-4">
    <h3 class="text-base font-semibold text-gray-800">{{ title }}</h3>

    <!-- Probabilité -->
    <div>
      <p class="text-sm text-gray-500 mb-1">Probabilité de défaut</p>
      <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div class="h-4 rounded-full transition-all duration-500"
          :class="barColor"
          :style="{ width: (result.probability * 100) + '%' }">
        </div>
      </div>
      <p class="text-right text-sm font-medium mt-1">{{ (result.probability * 100).toFixed(1) }}%</p>
    </div>

    <!-- Niveau de risque -->
    <div class="flex items-center gap-3">
      <span class="px-3 py-1 rounded-full text-sm font-semibold" :class="badgeClass">
        {{ result.risk_level }}
      </span>
    </div>

    <!-- Décision -->
    <div class="pt-2 border-t">
      <p class="text-sm text-gray-500">Décision de crédit</p>
      <p class="text-lg font-bold" :class="decisionColor">{{ result.credit_decision }}</p>
    </div>
  </div>
</template>

<script setup>
/**
 * Carte affichant le résultat d'un modèle (LR ou DT).
 * Props : title (string), result { probability, risk_level, credit_decision }.
 */
import { computed } from 'vue'


const props = defineProps({
  title: { type: String, required: true },
  result: { type: Object, required: true },
})


const badgeClass = computed(() => {
  if (props.result.risk_level === 'Safe')
    return 'bg-green-100 text-green-800'
  if (props.result.risk_level === 'Moyennement à risque')
    return 'bg-orange-100 text-orange-800'
  return 'bg-red-100 text-red-800'
})

const barColor = computed(() => {
  if (props.result.probability < 0.3) return 'bg-green-500'
  if (props.result.probability < 0.6) return 'bg-orange-400'
  return 'bg-red-500'
})

const decisionColor = computed(() => {
  if (props.result.credit_decision === 'Accepté totalement') return 'text-green-700'
  if (props.result.credit_decision === 'Accepté partiellement') return 'text-orange-600'
  return 'text-red-600'
})
</script>
