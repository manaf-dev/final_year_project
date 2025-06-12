import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
import router from '@/router';
import TokenService from '@/services/TokenServices';
import axios from 'axios';

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
                // Import apiClient dynamically to avoid circular dependency
                const { default: apiClient } = await import('../services/api');
                const response = await apiClient.get(`accounts/user/${this.user.id}/info/`)
                localStorage.setItem('user', JSON.stringify(response.data.user))
            } catch (error) {
                console.error(error)
            }
        },

        async login(credentials) {
            try {
                // Import apiClient dynamically to avoid circular dependency  
                const { default: apiClient } = await import('../services/api');
                const response = await apiClient.post('accounts/auth/login/', credentials);
                if (response.data) {
                    this.user = response.data.user || null;
                    this.accessToken = response.data.token?.access || null;
                    this.refreshToken = response.data.token?.refresh || null;

                    if (this.accessToken) {
                        TokenService.saveToken(this.accessToken);
                    }
                    if (this.refreshToken) {
                        TokenService.saveRefreshToken(this.refreshToken);
                    }
                    if (this.user) {
                        localStorage.setItem('user', JSON.stringify(this.user));
                    }

                    toast.success(response.data.detail || 'Login successful');
                    
                } else {
                    toast.error('Login failed');
                }
            } catch (error) {
                toast.error(error.response?.data?.detail || error.message || 'Login failed');
            }
        },

        async logout() {
            try {
                // Optional: Call logout endpoint if available
                // const { default: apiClient } = await import('../services/api');
                // await apiClient.post('accounts/auth/logout/');
                
                this.clearAuthData();
                toast.success('Logged out successfully');
                router.push('/login');
            } catch (error) {
                console.error('Logout error:', error);
                // Still clear auth data even if server call fails
                this.clearAuthData();
                router.push('/login');
            }
        },

        forceLogout() {
            // Used by interceptor when tokens are invalid
            this.clearAuthData();
            toast.error('Login session expired, please login again');
            router.push('/login');
        },

        clearAuthData() {
            // Clear all authentication data
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            TokenService.removeToken();
            TokenService.removeRefreshToken();
            localStorage.removeItem('user');
        },

        async refreshAccessToken() {
            console.log('Refreshing access token...');
            try {
                const baseURL = import.meta.env.VITE_API_BASE_URL;
                const response = await axios.post(`${baseURL}accounts/auth/token/refresh/`, {
                    refresh: this.refreshToken
                });
                
                console.log('Refresh response:', response);
                this.accessToken = response.data.access;
                this.refreshToken = response.data.refresh;
                TokenService.saveToken(this.accessToken);
                TokenService.saveRefreshToken(this.refreshToken);
                
                return response.data.access;
            } catch (error) {
                console.error('Error refreshing access token:', error);
                this.forceLogout();
                throw error;
            }
        },

        initializeAuth() {
            // Initialize auth state from stored tokens
            if (this.accessToken && this.refreshToken) {
                // Tokens are already set from state initialization
                console.log('Auth initialized with stored tokens');
            }
        }
    },
});
