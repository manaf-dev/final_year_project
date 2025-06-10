import { defineStore } from 'pinia';
import { useToast } from 'vue-toastification';
import apiClient from '../services/api';
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
                const response = await apiClient.get(`accounts/user/${this.user.id}/info/`)
                localStorage.setItem('user', JSON.stringify(response.data.user))
            } catch (error) {
                console.error(error)
            }
        },

        async login(credentials) {
            
            try {
                // console.log('axios', apiClient.headers.common['Authorization'])
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

                    toast.success(response.data.detail || 'Login successful');
                    
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
                // const response = await apiClient.post('accounts/auth/logout/')
                this.user = null;
                this.accessToken = null;
                this.refreshToken = null;
                localStorage.removeItem('user')
                localStorage.removeItem('accessToken')
                localStorage.removeItem('refreshToken')
                delete apiClient.defaults.headers['Authorization']
                router.push('/login')
            } catch (error) {
                toast.error('Logout failed')
            }
        },

        async refreshAccessToken() {
            console.log('Refreshing access token...');
            try {
                const baseURL = import.meta.env.VITE_API_BASE_URL;
                // console.log('axisos baseURL:', axios.baseURL);
                const response = await axios.post(`${baseURL}accounts/auth/token/refresh/`, {
                    refresh: this.refreshToken
                })
                console.log('Refresh response:', response);
                this.accessToken = response.data.access
                this.refreshToken = response.data.refresh
                localStorage.setItem('accessToken', this.accessToken)
                localStorage.setItem('refreshToken', this.refreshToken)
                // apiClient.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`
            } catch (error) {
                console.error('error refreshing access token:', error);
                toast.error('Login session expired, please login again');
                this.logout(); // Log the user out if refresh token is expired
            }
        },

        initializeAuth() {

            if (this.accessToken && this.refreshToken) {
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
            }
        }
    },
});
