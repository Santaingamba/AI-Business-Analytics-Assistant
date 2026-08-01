export interface User {
  id: string;
  email: string;
  username: string;
  display_name?: string;
  role: 'ADMIN' | 'USER' | 'ANALYST';
  status: 'ACTIVE' | 'INACTIVE' | 'LOCKED' | 'SUSPENDED' | 'PENDING_VERIFICATION';
  profile_image_url?: string;
  timezone: string;
  preferred_theme: string;
  preferred_language: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface UserCreate extends LoginData {
  username: string;
  display_name?: string;
}
