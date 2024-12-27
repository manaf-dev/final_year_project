import { defineStore } from 'pinia';
import { computed } from 'vue';
import { useToast } from 'vue-toastification';
import apiClient from '../services/api';
import router from '@/router';


const toast = useToast();

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
    }),

    getters: {
        isIntern: (state) => state.user?.account_type === 'intern',
        isAuthenticated: (state) => !!state.accessToken,
        hasProvidedDetails: (state) => !!state.user.intern_school
    },
    actions: {

        async getUserInfo() {
            try {
                const response = await apiClient.get(`accounts/user/${this.user.id}/info/`)
                localStorage.setItem('user', JSON.stringify(response.data.user))
            } catch (error) {
                console.log('error getting user infor', error)
            }
        },

        async login(credentials) {
            try {
                const response = await apiClient.post('accounts/auth/login/', credentials);
                this.user = response.data.user
                this.accessToken = response.data?.token?.access;
                this.refreshToken = response.data?.token?.refresh;

                apiClient.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`

                localStorage.setItem('accessToken', this.accessToken)
                localStorage.setItem('refreshToken', this.refreshToken)
                localStorage.setItem('user', JSON.stringify(this.user))

                toast.success(response.data.detail);
            } catch (error) {
                // console.log('DATA', error.response.data.detail)
                toast.error(error.response?.data?.detail || 'Login failed');
            }
        },

        async logout() {
            try {
                const response = await apiClient.post('accounts/auth/logout/')
                this.user = null;
                this.accessToken = null;
                this.refreshToken = null;
                localStorage.removeItem('user')
                localStorage.removeItem('accessToken')
                localStorage.removeItem('refreshToken')
                delete apiClient.defaults.headers.common['Authorization']
                router.push('/login')
                toast.success('Logout successful')
            } catch (error) {
                toast.error('Logout failed')
            }
        },

        async refreshAccessToken() {
            try {
                console.log('This is before request in refreshtoken')
                const response = await apiClient.post('accounts/auth/token/refresh/', {
                    refresh: this.refreshToken
                })
                console.log('This is after request in refreshtoken')
                this.accessToken = response.data.access
                apiClient.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`
                console.log('Refresh auth:', apiClient.defaults.headers['Authorization'])
                localStorage.setItem('accessToken', this.accessToken)
            } catch (error) {
                console.log('refresh token error before logout')
                this.logout()
                toast.info('Please Login again')
            }
        },

        initializeAuth() {

            if (this.accessToken && this.refreshToken) {
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
            }
        }
    },
});
