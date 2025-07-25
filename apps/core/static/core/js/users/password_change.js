// apps\core\static\core\js\users\password_change.js

import { fetchWithAuthOrRedirect, fetchWithAuth } from '/static/js/auth.js';

export async function initPasswordChange() {

    const response = await fetchWithAuthOrRedirect('/api/core/me/');

    root.innerHTML = `
      <div class="container mt-5" style="max-width: 400px;">
        <h2 class="mb-4 text-center">Đổi mật khẩu</h2>
        <div id="error-message" class="alert alert-danger d-none" role="alert"></div>
        <div id="success-message" class="alert alert-success d-none" role="alert"></div>

        <form id="password-change-form" novalidate>
          <div class="mb-3">
            <label for="old_password" class="form-label">Mật khẩu cũ</label>
            <input type="password" class="form-control" id="old_password" required />
          </div>
          <div class="mb-3">
            <label for="new_password1" class="form-label">Mật khẩu mới</label>
            <input type="password" class="form-control" id="new_password1" required />
          </div>
          <div class="mb-3">
            <label for="new_password2" class="form-label">Xác nhận mật khẩu mới</label>
            <input type="password" class="form-control" id="new_password2" required />
          </div>
          <button type="submit" class="btn btn-primary w-100">Đổi mật khẩu</button>
        </form>
      </div>
    `;

    const form = document.getElementById('password-change-form');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errorMessage.classList.add('d-none');
      successMessage.classList.add('d-none');
      errorMessage.textContent = '';
      successMessage.textContent = '';

      const old_password = document.getElementById('old_password').value.trim();
      const new_password1 = document.getElementById('new_password1').value.trim();
      const new_password2 = document.getElementById('new_password2').value.trim();

      if (!old_password || !new_password1 || !new_password2) {
        errorMessage.textContent = 'Vui lòng điền đầy đủ thông tin.';
        errorMessage.classList.remove('d-none');
        return;
      }

      if (new_password1 !== new_password2) {
        errorMessage.textContent = 'Mật khẩu mới không khớp.';
        errorMessage.classList.remove('d-none');
        return;
      }

      try {
        const response = await fetchWithAuth('/api/core/password-change/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ old_password, new_password1, new_password2 }),
        });

        if (!response) {
          return;
        }

        const text = await response.text();

        try {
          const data = JSON.parse(text);
          if (response.ok) {
            successMessage.textContent = data.detail || 'Đổi mật khẩu thành công.';
            successMessage.classList.remove('d-none');
            form.reset();
          } else {
            let errors = [];
            for (const key in data) {
              if (Array.isArray(data[key])) {
                errors.push(`${key}: ${data[key].join(', ')}`);
              } else {
                errors.push(`${key}: ${data[key]}`);
              }
            }
            errorMessage.innerHTML = errors.join('<br>');
            errorMessage.classList.remove('d-none');
          }
        } catch {
          errorMessage.textContent = 'Phản hồi không hợp lệ từ server.';
          errorMessage.classList.remove('d-none');
        }
      } catch (err) {
        errorMessage.textContent = 'Lỗi kết nối, vui lòng thử lại.';
        errorMessage.classList.remove('d-none');
        console.error(err);
      }
    });
  }
