import { jwtDecode } from 'jwt-decode';

export function isAuthenticated() {
  const token = localStorage.getItem('auth_token');
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    if (!decoded || !decoded.exp) return false;
    const now = Date.now() / 1000;
    return decoded.exp > now;
  } catch (e) {
    console.error('Invalid token:', e);
    return false;
  }
}
