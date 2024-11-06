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



apiClient.interceptors.request.use(request => {
    const accessToken = localStorage.getItem('accessToken')
    if (accessToken) {
        request.headers['Authorization'] = `Bearer ${accessToken}`
    }
    return request
}, error => {
    return Promise.reject(error)
})

// refresh token inceptor
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore()
        const originalRequest = error.config
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            try {
                await authStore.refreshAccessToken()
                return apiClient(originalRequest)
            } catch (refreshError) {
                authStore.logout()

            }
        }
        return Promise.reject(error)
    }
)


export default apiClient;