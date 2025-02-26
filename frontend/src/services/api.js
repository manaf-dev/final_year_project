import { useAuthStore } from '@/stores/auth';
import axios from 'axios';


const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json'
    },

});


// refresh token interceptor
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore();
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                await authStore.refreshAccessToken();
                originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
                return apiClient(originalRequest);
            } catch (refreshError) {
                if (refreshError.response && refreshError.response.status === 401) {
                    authStore.logout();
                }
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);


export default apiClient;