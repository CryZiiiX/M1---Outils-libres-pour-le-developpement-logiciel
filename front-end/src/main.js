/** Point d'entrée Vue : crée l'app, enregistre le router, monte sur #app. */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'


createApp(App).use(router).mount('#app')
