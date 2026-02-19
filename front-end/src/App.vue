<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <nav class="bg-white shadow">
      <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <router-link to="/" class="text-xl font-bold text-indigo-600">
          Credit Risk Predictor
        </router-link>
        <div class="flex gap-4">
          <router-link
            to="/"
            class="px-3 py-1 rounded text-sm font-medium"
            :class="$route.name === 'predict' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-600 hover:text-indigo-600'"
          >
            Prédiction
          </router-link>
          <router-link
            to="/history"
            class="px-3 py-1 rounded text-sm font-medium"
            :class="$route.name === 'history' || $route.name === 'detail' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-600 hover:text-indigo-600'"
          >
            Historique
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Contenu -->
    <main class="max-w-5xl mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>
