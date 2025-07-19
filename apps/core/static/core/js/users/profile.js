// apps\core\static\core\js\users\profile.js

import { fetchWithAuthOrRedirect } from '/static/js/auth.js';

export async function initProfile() {
  
  if (!root) return;

  root.innerHTML = `<p>Đang tải thông tin...</p>`;

  try {
    const response = await fetchWithAuthOrRedirect('/api/core/me/');
    const data = await response.json();

    root.innerHTML = `
    <div class="container my-4">
        <h2 class="mb-4 text-center">Thông tin tài khoản</h2>
        <div class="card shadow-sm">
        <div class="card-body">
            <div class="row mb-3">
            <div class="col-md-4 text-center">
                <img src="${data.profile_picture || '/static/images/default-avatar.png'}" alt="Ảnh đại diện" class="rounded-circle img-fluid" style="max-width:150px;" />
            </div>
            <div class="col-md-8">
                <ul class="list-group list-group-flush">
                <li class="list-group-item"><strong>Username:</strong> ${data.username}</li>
                <li class="list-group-item"><strong>Email:</strong> ${data.email}</li>
                <li class="list-group-item"><strong>Họ và tên:</strong> ${data.first_name || '(Chưa cập nhật)'} ${data.last_name || ''}</li>
                <li class="list-group-item"><strong>Số điện thoại:</strong> ${data.phone_number || '(Chưa cập nhật)'}</li>
                <li class="list-group-item"><strong>Ngày sinh:</strong> ${data.date_of_birth ? new Date(data.date_of_birth).toLocaleDateString() : '(Chưa cập nhật)'}</li>
                <li class="list-group-item"><strong>Địa chỉ:</strong> ${data.address || '(Chưa cập nhật)'}</li>
                <li class="list-group-item"><strong>Vai trò:</strong> ${data.role_display || data.role || '(Chưa cập nhật)'}</li>
                <li class="list-group-item"><strong>Ngày tham gia:</strong> ${data.date_joined ? new Date(data.date_joined).toLocaleDateString() : '(Chưa cập nhật)'}</li>
                <li class="list-group-item"><strong>Trạng thái xác thực:</strong> ${data.is_verified ? '<span class="text-success">Đã xác thực</span>' : '<span class="text-danger">Chưa xác thực</span>'}</li>
                </ul>
            </div>
            </div>

            <h3 class="mt-4">Danh sách nông trại</h3>
            ${
              data.farms && data.farms.length > 0
                ? `<div class="row row-cols-1 row-cols-md-3 g-3">
                    ${data.farms.map(farm => `
                    <div class="col">
                        <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${farm.name}</h5>
                            <p class="card-text mb-1"><strong>Vị trí:</strong> ${farm.location}</p>
                            <p class="card-text"><strong>Diện tích:</strong> ${farm.area} ha</p>
                        </div>
                        </div>
                    </div>
                    `).join('')}
                </div>`
                : '<p>Chưa có nông trại nào được liên kết.</p>'
            }
        </div>
        </div>
    </div>
    `;

  } catch (error) {
    console.error('Lỗi khi tải thông tin profile:', error);
    root.innerHTML = `<p>Đã có lỗi xảy ra. Vui lòng thử lại sau.</p>`;
  }
}
