import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from "primevue/config";
import Toast from "vue-toastification";
import 'primeicons/primeicons.css'
import "vue-toastification/dist/index.css";

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia();

app.use(pinia)
app.use(router)
app.use(PrimeVue);
app.use(Toast)


app.mount('#app')
