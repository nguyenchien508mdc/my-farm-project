
import { setupAutoRefresh } from '/static/js/auth.js';
export async function initLogin() {
  root.innerHTML = `
    <div class="container mt-5" style="max-width: 400px;">
      <h2 class="mb-4 text-center">Đăng nhập</h2>
      <div id="error-message" class="alert alert-danger d-none" role="alert"></div>
      <form id="login-form" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Tên đăng nhập</label>
          <input type="text" class="form-control" id="username" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Mật khẩu</label>
          <input type="password" class="form-control" id="password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Đăng nhập</button>
      </form>
      <div class="mt-3 text-center">
        <a href="/password-reset/">Quên mật khẩu?</a><br />
        <a href="/register/">Đăng ký tài khoản mới</a>
      </div>
    </div>
  `;

  const urlParams = new URLSearchParams(window.location.search);
  const nextPage = urlParams.get('next') || '/';

  const form = document.getElementById('login-form');
  const errorBox = document.getElementById('error-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorBox.classList.add('d-none');
    errorBox.textContent = '';

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (!username || !password) {
      errorBox.textContent = 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.';
      errorBox.classList.remove('d-none');
      return;
    }

    try {
      const response = await fetch('/api/core/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // gửi và nhận cookie HttpOnly
        body: JSON.stringify({ username, password }),
      });

      let data = {};
      try {
        data = await response.json();
      } catch {
        // Không nhận được JSON, có thể là lỗi server
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Đăng nhập thất bại');
      }
      setupAutoRefresh();
      window.location.href = nextPage;

    } catch (error) {
      errorBox.textContent = error.message;
      errorBox.classList.remove('d-none');
    }
  });
}
