import { renderSidebar } from './sidebar_render.js';
import { fetchWithAuth, clearToken, getAccessToken } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const sidebarRoot = document.getElementById('sidebar-root');
  const sidebarWrapper = document.querySelector('.navigation-sidebar');

  // Nếu không có token thì ẩn sidebar và return luôn
  const token = getAccessToken();
  if (!token) {
    if (sidebarWrapper) sidebarWrapper.style.display = 'none';
    return;
  }

  // Hàm gọi API lấy thông tin user
  async function fetchUser() {
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

  // Nếu không authenticated thì ẩn sidebar
  if (!user.isAuthenticated) {
    if (sidebarWrapper) sidebarWrapper.style.display = 'none';
    return;
  }

  // Render sidebar với user info
  if (sidebarRoot) {
    sidebarRoot.innerHTML = renderSidebar(user);
  }

});
