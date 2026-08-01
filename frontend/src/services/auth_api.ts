import { api } from './api';
import { User, UserCreate, LoginData, TokenResponse } from '../types/auth';

export const authApi = {
  login: async (data: LoginData) => {
    const response = await api.post<{ success: boolean; data: TokenResponse }>('/auth/login', data);
    return response.data;
  },
  register: async (data: UserCreate) => {
    const response = await api.post<{ success: boolean; data: User }>('/auth/register', data);
    return response.data;
  },
  logout: async () => {
    const response = await api.post<{ success: boolean }>('/auth/logout');
    return response.data;
  },
  refreshToken: async () => {
    const response = await api.post<{ success: boolean; data: TokenResponse }>('/auth/refresh');
    return response.data;
  },
  getMe: async () => {
    const response = await api.get<{ success: boolean; data: User }>('/users/me');
    return response.data;
  },
};
