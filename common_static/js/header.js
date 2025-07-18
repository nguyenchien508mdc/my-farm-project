// common_static\js\header.js
import { renderHeader } from './header_render.js';
import { getAccessToken } from './auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const headerRoot = document.getElementById('header-root');

  // Hàm gọi API lấy thông tin user
  async function fetchUser() {
    const token = getAccessToken();
    if (!token) return { isAuthenticated: false };

    try {
      const response = await fetch('/api/core/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        // Token hết hạn hoặc lỗi => xóa token
        localStorage.removeItem('access_token');
        return { isAuthenticated: false };
      }
      const data = await response.json();
      return {
        isAuthenticated: true,
        username: data.username,
        role: data.role,
        // thêm các trường khác nếu cần
      };
    } catch (error) {
      console.error('Lỗi khi lấy user:', error);
      return { isAuthenticated: false };
    }
  }

  const user = await fetchUser();

  // Render header
  headerRoot.innerHTML = renderHeader(user);

  // Xử lý logout
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    });
  }
});
