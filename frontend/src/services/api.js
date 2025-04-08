import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import TokenService from './TokenServices';


const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
});
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL);
// refresh token interceptor
apiClient.interceptors.request.use(
    (config) => {
        const accessToken = TokenService.getAccessToken();
        if (accessToken) {
            config.headers["Authorization"] = 'Bearer ' + accessToken
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore();
        const originalRequest = error.config;

        if (originalRequest.url !== '/login' && error.response) {

            if (error.response.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                try {
                    await authStore.refreshAccessToken();
                    originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
                    return apiClient(originalRequest);
                } catch (refreshError) {
                    return Promise.reject(refreshError);
                }
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;

