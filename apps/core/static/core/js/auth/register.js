// apps\core\static\js\auth\register.js
export async function initRegister() {

  root.innerHTML = `
    <div class="container mt-5" style="max-width: 400px;">
      <h2 class="mb-4 text-center">Đăng ký tài khoản mới</h2>

      <div id="error-message" class="alert alert-danger d-none" role="alert"></div>
      <div id="success-message" class="alert alert-success d-none" role="alert"></div>

      <form id="register-form" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Tên đăng nhập</label>
          <input type="text" class="form-control" id="username" name="username" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" name="email" required />
        </div>
        <div class="mb-3">
          <label for="password1" class="form-label">Mật khẩu</label>
          <input type="password" class="form-control" id="password1" name="password1" required />
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Xác nhận mật khẩu</label>
          <input type="password" class="form-control" id="password2" name="password2" required />
        </div>

        <button type="submit" class="btn btn-primary w-100">Đăng ký</button>
      </form>

      <div class="mt-3 text-center">
        <a href="/login/">Đã có tài khoản? Đăng nhập</a>
      </div>
    </div>
  `;

  const form = document.getElementById('register-form');
  const errorMessage = document.getElementById('error-message');
  const successMessage = document.getElementById('success-message');

  function showError(message) {
    errorMessage.innerHTML = message;
    errorMessage.classList.remove('d-none');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    errorMessage.classList.add('d-none');
    successMessage.classList.add('d-none');
    errorMessage.innerHTML = '';
    successMessage.innerHTML = '';

    const username = form.username.value.trim();
    const email = form.email.value.trim();
    const password1 = form.password1.value;
    const password2 = form.password2.value;

    if (!username || !email || !password1 || !password2) {
      showError('Vui lòng nhập đầy đủ thông tin.');
      return;
    }
    if (password1 !== password2) {
      showError('Mật khẩu và xác nhận mật khẩu không khớp.');
      return;
    }

    try {
      const response = await fetch('/api/core/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password: password1, password2 }),
      });

      if (response.ok) {
        successMessage.textContent = 'Đăng ký thành công! Bạn có thể đăng nhập ngay.';
        successMessage.classList.remove('d-none');
        form.reset();
        setTimeout(() => window.location.href = '/login/', 1000);
      } else {
        const data = await response.json();
        if (data && typeof data === 'object') {
          const errors = [];
          for (const key in data) {
            if (Array.isArray(data[key])) {
              errors.push(`${key}: ${data[key].join(', ')}`);
            } else {
              errors.push(`${key}: ${data[key]}`);
            }
          }
          showError(errors.join('<br>'));
        } else {
          showError('Có lỗi xảy ra, vui lòng thử lại.');
        }
      }
    } catch (err) {
      showError('Lỗi kết nối, vui lòng thử lại sau.');
      console.error(err);
    }
  });
};
