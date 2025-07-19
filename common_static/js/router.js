import { modules } from './modules.js';

const allRoutes = {};
let lastPath = null; // Đường dẫn cuối cùng đã init

/**
 * Load tất cả routes từ modules
 */
async function loadRoutes() {
  for (const loadModule of modules) {
    const mod = await loadModule();
    const routes = Object.values(mod).find(
      (v) => v && typeof v === 'object' && !Array.isArray(v)
    );
    if (routes) {
      Object.assign(allRoutes, routes);
    }
  }
}

/**
 * Chuẩn hóa đường dẫn: thêm dấu '/' ở cuối (trừ '/')
 */
function normalizePath(p) {
  return (p.length > 1 && !p.endsWith('/')) ? p + '/' : p;
}

/**
 * Thực thi route theo path
 */
async function handleRoute(path, root) {
  path = normalizePath(path);

  for (const pattern in allRoutes) {
    const isRegex = pattern.startsWith('^');
    const normalizedPattern = isRegex ? pattern : normalizePath(pattern);

    const matched = isRegex
      ? new RegExp(pattern).test(path)
      : normalizedPattern === path;

    if (matched) {
      const initFunc = await allRoutes[pattern]();
      if (typeof initFunc === 'function') {
        await initFunc(root);
        lastPath = path; // Cập nhật sau khi init thành công
      } else {
        console.warn(`Route init for ${pattern} is not a function.`);
      }
      return true;
    }
  }
  return false;
}

/**
 * Chuyển route bằng SPA
 */
export async function routeTo(path, root) {
  path = normalizePath(path);
  const currentPath = normalizePath(window.location.pathname);

  // Nếu path mới khác lastPath → xử lý
  if (path !== lastPath) {
    if (currentPath !== path) {
      history.pushState({}, '', path);
    }

    const handled = await handleRoute(path, root);
    if (!handled && root) {
      console.warn(`No route matched for path: ${path}`);
      root.innerHTML = '<h2>404 - Page Not Found</h2>';
    }
  } else {
    console.log(`Route ${path} đang hiển thị, bỏ qua init.`);
  }
}

// Khởi tạo SPA routing
document.addEventListener('DOMContentLoaded', async () => {
  await loadRoutes();

  const root = document.getElementById('root');
  const path = window.location.pathname;
  lastPath = normalizePath(path);

  await handleRoute(path, root);

  // Xử lý click vào link nội bộ
  document.addEventListener('click', async (e) => {
    const link = e.target.closest('a[data-link]');
    if (
      link &&
      link.origin === window.location.origin &&
      !link.hasAttribute('target')
    ) {
      e.preventDefault();
      const href = link.getAttribute('href');
      if (!href) return;

      await routeTo(href, root);
    }
  });

  // Xử lý back/forward
  window.addEventListener('popstate', async () => {
    const root = document.getElementById('root');
    const newPath = normalizePath(window.location.pathname);
    await handleRoute(newPath, root); // Luôn init lại nếu path khác lastPath
  });
});
