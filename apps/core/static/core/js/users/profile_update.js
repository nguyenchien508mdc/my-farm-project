// apps\core\static\core\js\users\profile_update.js

import { fetchWithAuthOrRedirect, clearToken} from '/static/js/auth.js';

export async function initProfileUpdate() {
  
  if (!root) return;

  root.innerHTML = `<p>Đang tải thông tin...</p>`;

  try {
    const response = await fetchWithAuthOrRedirect('/api/core/me/');

    const data = await response.json();

    root.innerHTML = `
      <div class="container my-4">
        <h2 class="mb-4 text-center">Thông tin tài khoản</h2>
        <form id="profile-form" class="card shadow-sm p-4">
          <div class="mb-3 text-center">
            <img src="${data.profile_picture || '/static/images/default-avatar.png'}" alt="Ảnh đại diện" class="rounded-circle img-fluid" style="max-width:150px;" />
          </div>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" id="username" class="form-control" value="${data.username}" disabled />
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" id="email" class="form-control" value="${data.email}" disabled />
          </div>
          <div class="mb-3">
            <label for="first_name" class="form-label">Họ</label>
            <input type="text" id="first_name" class="form-control" value="${data.first_name || ''}" />
          </div>
          <div class="mb-3">
            <label for="last_name" class="form-label">Tên</label>
            <input type="text" id="last_name" class="form-control" value="${data.last_name || ''}" />
          </div>
          <div class="mb-3">
            <label for="phone_number" class="form-label">Số điện thoại</label>
            <input type="text" id="phone_number" class="form-control" value="${data.phone_number || ''}" />
          </div>
          <div class="mb-3">
            <label for="date_of_birth" class="form-label">Ngày sinh</label>
            <input type="date" id="date_of_birth" class="form-control" value="${data.date_of_birth ? data.date_of_birth.split('T')[0] : ''}" />
          </div>
          <div class="mb-3">
            <label for="address" class="form-label">Địa chỉ</label>
            <input type="text" id="address" class="form-control" value="${data.address || ''}" />
          </div>

          <button type="submit" class="btn btn-primary w-100">Cập nhật thông tin</button>
          <div id="update-message" class="mt-3"></div>
        </form>
      </div>
    `;

    const form = document.getElementById('profile-form');
    const message = document.getElementById('update-message');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      message.textContent = '';
      message.className = '';

      const updatedData = {
        first_name: form.first_name.value.trim(),
        last_name: form.last_name.value.trim(),
        phone_number: form.phone_number.value.trim(),
        date_of_birth: form.date_of_birth.value || null,
        address: form.address.value.trim(),
      };

      try {
        const updateResponse = await fetchWithAuth('/api/core/me/', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updatedData),
        });

        if (!updateResponse) {
          message.textContent = 'Phiên đăng nhập hết hạn hoặc không hợp lệ. Vui lòng đăng nhập lại.';
          message.className = 'text-danger';
          clearToken();
          window.location.href = '/login';
          return;
        }

        if (!updateResponse.ok) {
          const errorData = await updateResponse.json();
          message.textContent = errorData.detail || 'Cập nhật thất bại.';
          message.className = 'text-danger';
          return;
        }

        message.textContent = 'Cập nhật thông tin thành công!';
        message.className = 'text-success';

      } catch (error) {
        message.textContent = 'Lỗi khi cập nhật thông tin. Vui lòng thử lại.';
        message.className = 'text-danger';
        console.error(error);
      }
    });

  } catch (error) {
    console.error('Lỗi khi tải thông tin profile:', error);
    root.innerHTML = `<p>Đã có lỗi xảy ra. Vui lòng thử lại sau.</p>`;
  }
}
