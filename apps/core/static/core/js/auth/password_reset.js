// apps\core\static\js\auth\password_reset.js
export async function initPasswordReset() {
  root.innerHTML = `
    <div class="container mt-5" style="max-width: 400px;">
      <h2 class="mb-4 text-center">Quên mật khẩu</h2>
      <div id="error-message" class="alert alert-danger d-none" role="alert"></div>
      <div id="success-message" class="alert alert-success d-none" role="alert"></div>
      <form id="password-reset-form" novalidate>
        <div class="mb-3">
          <label for="email" class="form-label">Email của bạn</label>
          <input type="email" class="form-control" id="email" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Gửi yêu cầu</button>
      </form>
      <div class="mt-3 text-center">
        <a href="/login/">Quay lại đăng nhập</a>
      </div>
    </div>
  `;

  const form = document.getElementById('password-reset-form');
  const errorMessage = document.getElementById('error-message');
  const successMessage = document.getElementById('success-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset thông báo
    errorMessage.classList.add('d-none');
    successMessage.classList.add('d-none');
    errorMessage.innerHTML = '';
    successMessage.textContent = '';

    const email = form.email.value.trim();
    if (!email) {
        errorMessage.textContent = 'Vui lòng nhập email.';
        errorMessage.classList.remove('d-none');
        return;
    }

    try {
        const response = await fetch('/api/core/password-reset/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
        });

        const raw = await response.text(); // lấy phản hồi dạng text

        try {
        const data = JSON.parse(raw); // thử parse text thành JSON

        if (response.ok) {
            successMessage.textContent = data.detail || 'Chúng tôi đã gửi hướng dẫn đặt lại mật khẩu.';
            successMessage.classList.remove('d-none');
            form.reset();
        } else {
            if (data.detail) {
            errorMessage.textContent = data.detail;
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
            }
            errorMessage.classList.remove('d-none');
        }

        } catch (parseError) {
        // Nếu không phải JSON (thường do server lỗi 500 trả về HTML)
        console.error('Phản hồi không hợp lệ JSON:', raw);
        throw new Error('Server trả về dữ liệu không hợp lệ.');
        }

    } catch (err) {
        console.error('Lỗi khi gửi yêu cầu:', err);
        errorMessage.textContent = 'Lỗi kết nối hoặc server, vui lòng thử lại sau.';
        errorMessage.classList.remove('d-none');
    }
    });

};

