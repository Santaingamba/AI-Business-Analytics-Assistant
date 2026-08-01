import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { User, LoginData } from '../types/auth';
import { authApi } from '../services/auth_api';
import { setAccessToken } from '../services/api';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: LoginData) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadUser = useCallback(async () => {
    try {
      const response = await authApi.refreshToken();
      if (response.success && response.data) {
        setAccessToken(response.data.access_token);
        const userRes = await authApi.getMe();
        if (userRes.success) {
          setUser(userRes.data);
        }
      }
    } catch (error) {
      setUser(null);
      setAccessToken(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();

    const handleUnauthorized = () => {
      setUser(null);
      setAccessToken(null);
    };

    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, [loadUser]);

  const login = async (data: LoginData) => {
    const response = await authApi.login(data);
    if (response.success && response.data) {
      setAccessToken(response.data.access_token);
      const userRes = await authApi.getMe();
      if (userRes.success) {
        setUser(userRes.data);
      }
    } else {
        throw new Error('Login failed');
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } finally {
      setUser(null);
      setAccessToken(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
