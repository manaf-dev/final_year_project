import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import RegisterView from '@/views/auth/RegisterView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SchoolDetailView from '@/views/auth/SchoolDetailView.vue'
import InternDashboardView from '@/views/intern/InternDashboardView.vue'
import FirstSubmissionView from '@/views/intern/FirstSubmissionView.vue'
import PortfolioView from '@/views/intern/PortfolioView.vue'
import SupervisorView from '@/views/intern/SupervisorView.vue'
import SchoolView from '@/views/intern/SchoolView.vue'
import SupervisorDashboardView from '@/views/supervisor/SupervisorDashboardView.vue'
import ProfileView from '@/views/ProfileView.vue'
import FirstMonth from '@/views/supervisor/FirstMonthView.vue'
import PastSubmissions from '@/views/supervisor/PastSubmissions.vue'
import PortfolioDetailView from '@/views/supervisor/PortfolioDetailView.vue'
import MentorDetailView from '@/views/auth/MentorDetailView.vue'



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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true, }
    },
    {
      path: '/in/dashboard',
      name: 'intern-dashboard',
      component: InternDashboardView,
      meta: { requiresAuth: true, internOnly: true }
    },
    {
      path: '/in/submission/:month',
      name: 'first-submission',
      component: FirstSubmissionView,
      meta: { requiresAuth: true, internOnly: true }
    },

    {
      path: '/in/portfolio',
      name: 'intern-portfolio',
      component: PortfolioView,
      meta: { requiresAuth: true, internOnly: true }
    },
    {
      path: '/in/supervisor',
      name: 'intern-supervisor',
      component: SupervisorView,
      meta: { requiresAuth: true, internOnly: true }
    },
    {
      path: '/in/school',
      name: 'intern-school',
      component: SchoolView,
      meta: { requiresAuth: true, internOnly: true }
    },

    {
      path: '/sp/dashboard',
      name: 'supervisor-dashboard',
      component: SupervisorDashboardView,
      meta: { requiresAuth: true, supervisorOnly: true }
    },
    {
      path: '/sp/submissions/:month',
      name: 'submissions-first',
      component: FirstMonth,
      meta: { requiresAuth: true, supervisorOnly: true }
    },
    {
      path: '/sp/submission/:intern/:month',
      name: 'submission-detail',
      component: PortfolioDetailView,
      meta: { requiresAuth: true, supervisorOnly: true }
    },
    {
      path: '/sp/submissions/past',
      name: 'past-submissions',
      component: PastSubmissions,
      meta: { requiresAuth: true, supervisorOnly: true }
    },
    {
      path: '/school',
      name: 'school',
      component: SchoolDetailView,
      meta: { requiresAuth: true, internOnly: true }
    },
    {
      path: '/mentor',
      name: 'mentor',
      component: MentorDetailView,
      meta: { requiresAuth: true, internOnly: true }
    },

  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.guest && authStore.isAuthenticated) {
    if (authStore.isIntern) {
      return next({ name: 'intern-dashboard' })
    } else {
      return next({ name: 'supervisor-dashboard' })

    }
  }

  if (to.meta.internOnly && !authStore.isIntern) {
    console.log('from', from)
    console.log('to', to)
    return next(from)
  }



  next()
})

export default router
