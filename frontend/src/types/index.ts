// Types pour l'utilisateur
export interface User {
    id: number;
    nom: string;
    prenom: string;
    email: string;
    role: string;
    is_active: boolean;
    date_creation: string;
    date_modification: string;
  }
  
  // Types pour l'authentification
  export interface AuthState {
    user: User | null;
    token: string | null;
    loading: boolean;
    error: string | null;
    isAuthenticated: boolean;
  }
  
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface LoginResponse {
    token: string;
    user: User;
  }
  
  // Types pour les erreurs API
  export interface ApiError {
    error: string;
  }