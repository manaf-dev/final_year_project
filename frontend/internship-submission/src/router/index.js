import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/auth/LoginView.vue'
import SchoolDetailView from '@/views/auth/SchoolDetailView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import DasboardView from '@/views/DasboardView.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DasboardView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/school',
      name: 'school',
      component: SchoolDetailView
    },

  ]
})

export default router
