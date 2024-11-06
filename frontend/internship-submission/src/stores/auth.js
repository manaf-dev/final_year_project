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
        isIntern: (state) => state.user.account_type === 'intern',
        isAuthenticated: (state) => !!state.accessToken,
        hasProvidedDetails: (state) => !!state.user.intern_school
    },
    actions: {
        async register(userData) {
            try {
                const response = await apiClient.post('accounts/auth/registration/', userData);
                router.push('/login')

                toast.success(response.data.detail);
            } catch (error) {
                console.log('REG ERROR:', error)
                toast.error(error.response?.data?.detail || error.response?.data?.username[0] || 'Registration failed');
            }
        },

        async login(credentials) {
            try {
                const response = await apiClient.post('accounts/auth/login/', credentials);
                this.user = response.data.user
                this.accessToken = response.data?.token?.access;
                this.refreshToken = response.data?.token?.refresh;

                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`

                localStorage.setItem('accessToken', this.accessToken)
                localStorage.setItem('refreshToken', this.refreshToken)
                localStorage.setItem('user', JSON.stringify(this.user))

                toast.success(response.data.detail);
            } catch (error) {
                // console.log('DATA', error.response.data.detail)
                toast.error(error.response?.data?.detail || 'Login failed');
            }
        },

        logout() {
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            localStorage.removeItem('user')
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
            delete axios.defaults.headers.common['Authorization']
        },

        async refreshAccessToken() {
            try {
                const response = await apiClient.post('accounts/auth/token/refresh/', {
                    refresh: this.refreshToken
                })
                this.accessToken = response.data.access
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
                localStorage.setItem('accessToken', this.accessToken)
            } catch (error) {
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
