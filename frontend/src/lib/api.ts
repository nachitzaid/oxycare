import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

// Définir l'URL de base de l'API
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token aux requêtes
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs des réponses
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    const originalRequest = error.config;
    
    // Si erreur 401 (non autorisé), rediriger vers la page de connexion
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Fonction utilitaire pour les requêtes API
export const apiService = {
  async login(credentials: { email: string; password: string }) {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  
  async getMe() {
    const response = await api.get('/auth/me');
    return response.data;
  },
  
  async get(url: string, params?: any) {
    const response = await api.get(url, { params });
    return response.data;
  },
  
  async post(url: string, data: any) {
    const response = await api.post(url, data);
    return response.data;
  },
  
  async put(url: string, data: any) {
    const response = await api.put(url, data);
    return response.data;
  },
  
  async delete(url: string) {
    const response = await api.delete(url);
    return response.data;
  }
};