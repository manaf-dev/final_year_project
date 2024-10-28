import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    },
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
});

export default apiClient;


// apiClient.interceptors.response.use(
//     response => response,
//     async (error) => {
//         const authStore = useAuthStore()
//         const originalRequest = error.config

//         if (error.response.status === 401 && !originalRequest._retry) {
//             await authStore.refreshAccessToken()
//             originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`
//             return apiClient(originalRequest)
//         }
//     }
// )
