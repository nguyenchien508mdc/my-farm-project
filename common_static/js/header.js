import { renderHeader } from './header_render.js';
import { fetchWithAuth, logout } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const headerRoot = document.getElementById('header-root');

  async function fetchUser() {
    try {
      const response = await fetchWithAuth('/api/core/me', {
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response || !response.ok) {
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
      return { isAuthenticated: false };
    }
  }

  async function renderUser() {
    const user = await fetchUser();
    headerRoot.innerHTML = renderHeader(user);

    // Gắn sự kiện logout nếu có nút logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        await logout(); // Gọi API logout và xóa cookie
      });
    }
  }

  await renderUser();
});
