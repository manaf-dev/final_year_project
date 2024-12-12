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



// apiClient.interceptors.request.use(request => {
//     const accessToken = localStorage.getItem('accessToken')
//     console.log('URL', request.url)
//     if (request.url !== 'accounts/auth/token/refresh/') {
//         request.headers['Authorization'] = `Bearer ${accessToken}`
//     }
//     return request
// }, error => {
//     return Promise.reject(error)
// })

// refresh token inceptor
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const authStore = useAuthStore()
        const originalRequest = error.config
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            try {
                console.log('This is before refresh in interceptor')
                await authStore.refreshAccessToken()
                console.log('This is before authorization in interceptor')
                originalRequest.headers['Authorization'] = `Bearer ${localStorage.getItem('accessToken')}`;
                console.log('interceptor auth:', originalRequest.headers['Authorization'])
                return apiClient(originalRequest)
            } catch (refreshError) {
                console.log('This is before logout in interceptor')
                authStore.logout()
                console.log('This is after logout in interceptor')
            }
        }
        return Promise.reject(error)
    }
)


export default apiClient;