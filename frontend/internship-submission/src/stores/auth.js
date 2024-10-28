import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { useToast } from 'vue-toastification';
import router from '@/router';

const toast = useToast();

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: localStorage.getItem('user') || null,
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
        isAuthenticated: !!localStorage.getItem('accessToken')

    }),
    actions: {
        async register(userData) {
            try {
                const response = await apiClient.post('accounts/auth/registration/', userData);
                router.push('/login')

                toast.success(response.data.detail);
            } catch (error) {
                toast.error(response.data.detail);
            }
        },
        async login(credentials) {
            try {
                const response = await apiClient.post('accounts/auth/login/', credentials);
                this.user = response.data.user
                localStorage.setItem('user', JSON.stringify(this.user))
                this.setTokens(response.data.token.access, response.data.token.refresh)
                this.redirect()
                toast.success(response.data.detail);
            } catch (error) {
                // console.log('DATA', error.response.data.detail)
                toast.error(error.response.data.detail);
            }
        },
        logout() {
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            localStorage.removeItem('user')
            localStorage.setItem('accessToken')
            localStorage.setItem('refreshToken')
            toast.success('Logged out successfully!');
        },
        async refreshAccessToken() {
            const response = await apiClient.post('accounts/auth/refresh', { refresh: this.refreshToken })
            this.accessToken = response.data.access
            localStorage.setItem('accessToken', this.accessToken)
        },
        async setTokens(access, refresh) {
            this.accessToken = access;
            this.refreshToken = refresh;
            localStorage.setItem('accessToken', access)
            localStorage.setItem('refreshToken', refresh)
            this.isAuthenticated = true
        },
        redirect() {
            if (this.isAuthenticated && this.accessToken) {
                if (this.user.intern_account) {
                    if (this.user.intern_school) {
                        router.push("/dashboard");
                    } else {
                        router.push("/school");
                    }
                } else {
                    router.push("/dashboard");
                }
            } else router.push("/login");
        },
        async updateUser(userData) {
            const userId = localStorage.getItem('user.pk')
            try {
                const response = await apiClient.put(`accounts/auth/user/${userId}/`, userData)

            } catch (error) {
                console.log('Update Error:', error)
            }
        },
    },
});
