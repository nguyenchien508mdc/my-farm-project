// common_static\js\header.js
import { renderHeader } from './header_render.js';
import { fetchWithAuth, clearToken, getAccessToken, logout } from '/static/js/auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const headerRoot = document.getElementById('header-root');

  // Hàm gọi API lấy thông tin user, dùng fetchWithAuth tự động xử lý token
  async function fetchUser() {
    const token = getAccessToken();
    if (!token) return { isAuthenticated: false };

    try {
      const response = await fetchWithAuth('/api/core/me', {
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response || !response.ok) {
        clearToken();
        return { isAuthenticated: false };
      }

      const data = await response.json();
      return {
        isAuthenticated: true,
        username: data.username,
        role: data.role,
      };
    } catch (error) {
      console.error('Lỗi khi lấy user:', error);
      clearToken();
      return { isAuthenticated: false };
    }
  }

  const user = await fetchUser();

  // Render header theo thông tin user
  headerRoot.innerHTML = renderHeader(user);

  // Gắn sự kiện logout nếu có nút logout
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      logout(); 
    });
  }
});
