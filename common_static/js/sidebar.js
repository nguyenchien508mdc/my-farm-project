import { renderSidebar } from './sidebar_render.js';
import { getAccessToken, parseJwt } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
  const sidebarRoot = document.getElementById('sidebar-root');
  const sidebarWrapper = document.querySelector('.navigation-sidebar');

  const token = getAccessToken();

  if (!token) {
    if (sidebarWrapper) {
      sidebarWrapper.style.display = 'none'; 
    }
    return;
  }

  try {
    const payload = parseJwt(token);
    const user = {
      isAuthenticated: true,
      username: payload.username || '',
      role: payload.role || '',
    };

    if (sidebarRoot) {
      sidebarRoot.innerHTML = renderSidebar(user);
    }
  } catch (err) {
    console.error('Không thể parse JWT:', err);
    if (sidebarWrapper) {
      sidebarWrapper.style.display = 'none';
    }
  }
});
