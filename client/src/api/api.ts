import axios from "axios"
// Import your Pinia store to clear state on forced logout
import { useAuthStore } from '../stores/auth'

const BASE_URL = "http://127.0.0.1:8000/api" 

const api = axios.create({
    baseURL: `${BASE_URL}`,
    headers: {
        "Content-Type": "application/json",
    }
})

api.interceptors.request.use(
    (config) => {
        const accessToken = localStorage.getItem("access_token")
        if (accessToken) {
            config.headers["Authorization"] = `Bearer ${accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
)

// Handle 401 errors and refresh token
api.interceptors.response.use(
  (response) => response, 
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (!refreshToken) {
          handleLogout();
          return Promise.reject(error);
        }

        // Request a new access token using the refresh token
        const response = await axios.post(`${BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken, 
        });

        const { access, refresh } = response.data;

        localStorage.setItem('access_token', access);
        if (refresh) {
          localStorage.setItem('refresh_token', refresh);
        }

        originalRequest.headers['Authorization'] = `Bearer ${access}`;

        // Retry the original request
        return api(originalRequest);
        
      } catch (refreshError) {
        handleLogout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

const handleLogout = () => {
    // 1. Purge LocalStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('auth_user');
    
    // 2. Clear Pinia UI state safely (if initialized)
    try {
        const authStore = useAuthStore()
        authStore.currentUser = null
    } catch (e) {
        // App hasn't finished mounting yet, fallback safely
    }

    // 3. Redirect
    if (window.location.pathname !== '/login') {
        window.location.href = '/login';
    }
}

export default api
