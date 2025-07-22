import { renderSidebar } from './sidebar_render.js';
import { fetchWithAuth } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const sidebarWrapper = document.querySelector('.navigation-sidebar');
  const sidebarRoot = document.getElementById('sidebar-root');

  async function fetchUser() {
    try {
      const response = await fetchWithAuth('/api/core/me', {
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response || !response.ok) {
        throw new Error('Không xác thực được');
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

  const user = await fetchUser();

  if (user.isAuthenticated) {
    sidebarRoot.innerHTML = renderSidebar(user);
    sidebarWrapper.style.display = 'block';
  } else {
    sidebarRoot.innerHTML = "";
    sidebarWrapper.style.display = 'none';
  }
});
