import axios from 'axios';
import TokenService from './TokenServices';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
});

// Request interceptor to add Authorization header
apiClient.interceptors.request.use(
    (config) => {
        const accessToken = TokenService.getAccessToken();
        if (accessToken) {
            config.headers["Authorization"] = 'Bearer ' + accessToken;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh the token
                const refreshToken = TokenService.getRefreshToken();
                if (!refreshToken) {
                    throw new Error('No refresh token available');
                }

                const baseURL = import.meta.env.VITE_API_BASE_URL;
                const response = await axios.post(`${baseURL}accounts/auth/token/refresh/`, {
                    refresh: refreshToken
                });

                // Update tokens
                const newAccessToken = response.data.access;
                const newRefreshToken = response.data.refresh;
                
                TokenService.saveToken(newAccessToken);
                TokenService.saveRefreshToken(newRefreshToken);

                // Retry original request with new token
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                return apiClient(originalRequest);
            } catch (refreshError) {
                // Refresh failed - logout user
                console.error('Token refresh failed:', refreshError);
                TokenService.removeToken();
                TokenService.removeRefreshToken();
                localStorage.removeItem('user');
                
                // Import auth store dynamically to avoid circular dependency
                const { useAuthStore } = await import('@/stores/auth');
                const authStore = useAuthStore();
                authStore.forceLogout();
                
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;

