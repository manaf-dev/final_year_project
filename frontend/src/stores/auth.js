import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
import apiClient from '../services/api';
import router from '@/router';
import TokenService from '@/services/TokenServices';


const toast = useToast();

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        accessToken: TokenService.getAccessToken(),
        refreshToken: TokenService.getRefreshToken(),
    }),

    getters: {
        isIntern: (state) => state.user?.account_type === 'intern',
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {

        async getUserInfo() {
            try {
                const response = await apiClient.get(`accounts/user/${this.user.id}/info/`)
                localStorage.setItem('user', JSON.stringify(response.data.user))
            } catch (error) {
                console.error(error)
            }
        },

        async login(credentials) {
            try {
                const response = await apiClient.post('accounts/auth/login/', credentials);
                if (response.data) {
                    this.user = response.data.user || null;
                    this.accessToken = response.data.token?.access || null;
                    this.refreshToken = response.data.token?.refresh || null;

                    if (this.accessToken) {
                        apiClient.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`;
                        TokenService.saveToken(this.accessToken);
                    }
                    if (this.refreshToken) {
                        TokenService.saveRefreshToken(this.refreshToken);
                    }
                    if (this.user) {
                        localStorage.setItem('user', JSON.stringify(this.user));
                    }

                    if (response.data.detail) {
                        toast.success(response.data.detail);
                    }
                } else {
                    toast.error('Login failed');
                }
            } catch (error) {
                // console.log('DATA--', error);
                toast.error(error.response?.data?.detail || error.message || 'Login failed');
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
            } catch (error) {
                toast.error('Logout failed')
            }
        },

        async refreshAccessToken() {
            try {
                const response = await apiClient.post('accounts/auth/token/refresh/', {
                    refresh: this.refreshToken
                })
                this.accessToken = response.data.access
                localStorage.setItem('accessToken', this.accessToken)
                apiClient.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`
            } catch (error) {
                console.error(error)
            }
        },

        initializeAuth() {

            if (this.accessToken && this.refreshToken) {
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
            }
        }
    },
});
