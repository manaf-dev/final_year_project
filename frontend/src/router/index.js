import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import InternDashboardView from '@/views/intern/InternDashboardView.vue'
import MonthPortfolio from '@/views/intern/MonthPortfolioView.vue'
import TotalPortfolio from '@/views/intern/TotalPortfolioView.vue'
import SupervisorView from '@/views/intern/SupervisorView.vue'
import SupervisorDashboardView from '@/views/supervisor/SupervisorDashboardView.vue'
import ProfileView from '@/views/ProfileView.vue'
import MonthSubmissions from '@/views/supervisor/MonthSubmissionsView.vue'
import PastSubmissions from '@/views/supervisor/PastSubmissions.vue'
import PortfolioDetailView from '@/views/supervisor/PortfolioDetailView.vue'
import CohortList from '@/views/supervisor/CohortList.vue'
import CohortDetail from '@/views/supervisor/CohortDetail.vue'
import PastSubmissionsMonths from '@/views/supervisor/PastSubmissionsMonths.vue'
import PastSubmissionsInterns from '@/views/supervisor/PastSubmissionsInterns.vue'
import Notifications from '@/views/Notifications.vue'
import ScoresView from '@/views/supervisor/ScoresView.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { guest: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/reset/password',
      name: 'password-reset',
      component: () => import('@/views/auth/ResetPasswordEmail.vue'),
      meta: { guest: true }
    },
    {
      path: '/reset/password/email-sent',
      name: 'email-sent',
      component: () => import('@/views/auth/EmailSentView.vue'),
      meta: { guest: true }
    },
    {
      path: '/reset/password/new/:token',
      name: 'new-password',
      component: () => import('@/views/auth/ResetNewPassword.vue'),
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
      meta: { requiresAuth: true, internsOnly: true }
    },
    {
      path: '/in/submission/:month',
      name: 'submissions-page',
      component: MonthPortfolio,
      meta: { requiresAuth: true, internsOnly: true }
    },

    {
      path: '/in/portfolio',
      name: 'intern-portfolio',
      component: TotalPortfolio,
      meta: { requiresAuth: true, internsOnly: true }
    },
    {
      path: '/in/supervisor',
      name: 'intern-supervisor',
      component: SupervisorView,
      meta: { requiresAuth: true, internsOnly: true }
    },
    {
      path: '/sp/dashboard',
      name: 'supervisor-dashboard',
      component: SupervisorDashboardView,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/submissions/:month',
      name: 'submissions-list',
      component: MonthSubmissions,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/submission/:intern/:month',
      name: 'submission-detail',
      component: PortfolioDetailView,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/scores',
      name: 'scores',
      component: ScoresView,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/past/submissions/cohorts',
      name: 'past-submissions-cohorts',
      component: PastSubmissions,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/past/:year/months',
      name: 'past-submissions-months',
      component: PastSubmissionsMonths,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/past/:year/:month/interns',
      name: 'past-submissions-interns',
      component: PastSubmissionsInterns,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/dashboard/cohorts',
      name: 'cohorts-list',
      component: CohortList,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/sp/dashboard/cohorts/:year',
      name: 'cohort-detail',
      component: CohortDetail,
      meta: { requiresAuth: true, supervisorsOnly: true }
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: Notifications,
      meta: { requiresAuth: true }
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue')
    },
    {
      path: '/server-error',
      name: 'server-error',
      component: () => import('@/views/ServerErrorView.vue'),
      meta: { guest: true }
    }
  ]
})


router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.path === '/') {
    if (!authStore.isAuthenticated) {
      return next({ name: 'login' })
    } else {
      if (authStore.isIntern) {
        return next({ name: 'intern-dashboard' })
      } else {
        return next({ name: 'supervisor-dashboard' })
      }
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (to.meta.guest && authStore.isAuthenticated) {
    if (authStore.isIntern) {
      return next({ name: 'intern-dashboard' })
    } else {
      return next({ name: 'supervisor-dashboard' })

    }
  }

  if (to.meta.internsOnly && !authStore.isIntern) {
    // console.log('from', from)
    // console.log('to', to)
    return next({ name: 'supervisor-dashboard' })
  }

  if (to.meta.supervisorsOnly && authStore.isIntern) {
    return next({ name: 'intern-dashboard' })
  }


  next()
})

export default router
