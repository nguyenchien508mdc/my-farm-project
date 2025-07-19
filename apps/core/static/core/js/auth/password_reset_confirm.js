// apps/core/static/js/auth/password_reset_confirm.js

export async function initPasswordResetConfirm() {
  const pathParts = window.location.pathname.split('/').filter(Boolean);

  const uid = pathParts[1]; // reset/<uid>/<token>/
  const token = pathParts[2];

  root.innerHTML = `
    <div class="container mt-5" style="max-width: 400px;">
      <h2 class="mb-4 text-center">Đặt lại mật khẩu</h2>
      <div id="error-message" class="alert alert-danger d-none" role="alert"></div>
      <div id="success-message" class="alert alert-success d-none" role="alert"></div>

      <form id="reset-confirm-form" novalidate>
        <div class="mb-3">
          <label for="new_password1" class="form-label">Mật khẩu mới</label>
          <input type="password" class="form-control" id="new_password1" required />
        </div>
        <div class="mb-3">
          <label for="new_password2" class="form-label">Xác nhận mật khẩu</label>
          <input type="password" class="form-control" id="new_password2" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Đặt lại mật khẩu</button>
      </form>

      <div class="mt-3 text-center">
        <a href="/login/">Quay lại đăng nhập</a>
      </div>
    </div>
  `;

  const form = document.getElementById('reset-confirm-form');
  const errorMessage = document.getElementById('error-message');
  const successMessage = document.getElementById('success-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMessage.classList.add('d-none');
    successMessage.classList.add('d-none');
    errorMessage.innerHTML = '';
    successMessage.textContent = '';

    const new_password1 = document.getElementById('new_password1').value.trim();
    const new_password2 = document.getElementById('new_password2').value.trim();

    if (!new_password1 || !new_password2) {
      errorMessage.textContent = 'Vui lòng nhập đầy đủ mật khẩu.';
      errorMessage.classList.remove('d-none');
      return;
    }

    if (new_password1 !== new_password2) {
      errorMessage.textContent = 'Mật khẩu không khớp.';
      errorMessage.classList.remove('d-none');
      return;
    }

    try {
      const response = await fetch('/api/core/password-reset-confirm/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, token, new_password1, new_password2 })
      });

      const raw = await response.text();

      try {
        const data = JSON.parse(raw);

        if (response.ok) {
          successMessage.textContent = data.detail || 'Mật khẩu của bạn đã được thay đổi.';
          successMessage.classList.remove('d-none');
          form.remove(); // ẩn form
        } else {
          let errors = [];
          for (const key in data) {
            errors.push(`${key}: ${data[key].join(', ')}`);
          }
          errorMessage.innerHTML = errors.join('<br>');
          errorMessage.classList.remove('d-none');
        }
      } catch (err) {
        console.error('Không thể phân tích phản hồi:', raw);
        errorMessage.textContent = 'Lỗi máy chủ. Vui lòng thử lại.';
        errorMessage.classList.remove('d-none');
      }
    } catch (err) {
      console.error(err);
      errorMessage.textContent = 'Không thể kết nối đến máy chủ.';
      errorMessage.classList.remove('d-none');
    }
  });
};
