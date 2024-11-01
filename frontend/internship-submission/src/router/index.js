import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/auth/LoginView.vue'
import SchoolDetailView from '@/views/auth/SchoolDetailView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import DashboardView from '@/views/DasboardView.vue'
import InternDashboardView from '@/views/intern/InternDashboardView.vue'
import SupervisorDashboard from '@/views/SupervisorDashboard.vue'
import { useAuthStore } from '@/stores/auth'
import InternSubmissionsView from '@/views/intern/InternSubmissionsView.vue'
import PortfolioView from '@/views/intern/PortfolioView.vue'
import SupervisorView from '@/views/intern/SupervisorView.vue'
import SchoolView from '@/views/intern/SchoolView.vue'
import MentorView from '@/views/intern/MentorView.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guest: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guest: true }
    },
    {
      path: '/in/dashboard',
      name: 'intern-dashboard',
      component: InternDashboardView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/in/submissions',
      name: 'intern-submissions',
      component: InternSubmissionsView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/in/portfolio',
      name: 'intern-portfolio',
      component: PortfolioView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/in/supervisor',
      name: 'intern-supervisor',
      component: SupervisorView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/in/school',
      name: 'intern-school',
      component: SchoolView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/in/mentor',
      name: 'intern-mentor',
      component: MentorView,
      meta: { requiresAuth: true, requiresInternDetails: true }
    },
    {
      path: '/sp/dashboard',
      name: 'supervisor-dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/school',
      name: 'school',
      component: SchoolDetailView,
      meta: { requiresAuth: true }
    },

  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  // if (to.meta.guest && authStore.isAuthenticated) {
  //   return next('/dashboard')
  // }

  // if (to.meta.requiresInternDetails && authStore.isIntern && !authStore.hasProvidedDetails) {
  //   return next('/school')
  // }

  // if (to.meta.isSupervisor && !authStore.isSupervisor) {
  //   return next('/dashboard')
  // }

  next()
})

export default router
