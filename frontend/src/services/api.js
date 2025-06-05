import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import TokenService from './TokenServices';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
});

// apiClient.interceptors.request.use(
//     (config) => {
//         const accessToken = TokenService.getAccessToken();
//         console.log('Access Token:', accessToken);
//         console.log('Config Headers:', config.headers);
//         if (accessToken) {
//             config.headers["Authorization"] = 'Bearer ' + accessToken;
//         }
//         return config;
//     },
//     (error) => {
//         return Promise.reject(error);
//     }
// );

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore();
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                await authStore.refreshAccessToken();
                originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`;
                return apiClient(originalRequest);
            } catch (refreshError) {
                
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;

