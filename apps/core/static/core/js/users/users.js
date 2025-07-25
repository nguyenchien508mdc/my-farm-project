import {
  fetchAllUsers,
  createUser,
  updateUser,
  deleteUser
} from '../api/userAPI.js';
import { showAlert } from '/static/js/alerts.js';

export async function initUsers(root) {
  await renderUserList(root);
}

async function renderUserList(root) {
  try {
    const users = await fetchAllUsers();

    root.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>Danh sách người dùng</h2>
        <button class="btn btn-primary" id="btn-add-user">+ Thêm người dùng</button>
      </div>

      <table class="table table-striped table-bordered align-middle">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Họ tên</th>
            <th>Email</th>
            <th>SĐT</th>
            <th>Địa chỉ</th>
            <th>Vai trò</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          ${users.map(user => `
            <tr>
              <td>${user.id}</td>
              <td class="d-flex align-items-center">
                <img src="${user.profile_picture || '/static/img/avatar-placeholder.png'}" class="rounded-circle me-2" width="40" height="40" />
                <span>${user.first_name || ''} ${user.last_name || ''}</span>
              </td>
              <td>${user.email}</td>
              <td>${user.phone_number || ''}</td>
              <td>${user.address || ''}</td>
              <td>${user.role_display || user.role}</td>
              <td>
                <button class="btn btn-sm btn-warning me-1 btn-edit" data-id="${user.id}">Sửa</button>
                <button class="btn btn-sm btn-danger btn-delete" data-id="${user.id}">Xóa</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div id="user-form-overlay"></div>
    `;

    root.querySelectorAll('.btn-edit').forEach(btn => {
      btn.onclick = () => handleEditUser(btn.dataset.id, root);
    });

    root.querySelectorAll('.btn-delete').forEach(btn => {
      btn.onclick = () => handleDeleteUser(btn.dataset.id, root);
    });

    document.getElementById('btn-add-user').onclick = () => renderUserForm(null, root);
  } catch (err) {
    showAlert('error', err.message || 'Lỗi tải danh sách người dùng');
  }
}

function renderUserForm(user = null, root) {
    const container = document.getElementById('user-form-overlay');
    container.innerHTML = `
        <div class="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50 d-flex justify-content-center align-items-center" style="z-index: 1050; overflow-y: auto; padding: 1rem;">
        <div class="card shadow-lg" style="min-width: 400px; max-width: 600px; max-height: 90vh; overflow-y: auto;">
            <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">${user ? 'Cập nhật' : 'Thêm'} người dùng</h5>
            <button type="button" class="btn-close" id="cancel-user-form"></button>
            </div>
            <div class="card-body">
            <form id="user-form">
                <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Tên đăng nhập</label>
                    <input type="text" class="form-control" name="username" value="${user?.username || ''}" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Vai trò</label>
                    <select class="form-select" name="role" required>
                    <option value="admin" ${user?.role === 'admin' ? 'selected' : ''}>Quản trị viên</option>
                    <option value="staff" ${user?.role === 'staff' ? 'selected' : ''}>Nhân viên</option>
                    <option value="customer" ${user ? (user.role === 'customer' ? 'selected' : '') : 'selected'}>Khách hàng</option>
                    </select>
                </div>

                <div class="col-md-6">
                    <label class="form-label">Họ</label>
                    <input type="text" class="form-control" name="first_name" value="${user?.first_name || ''}" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Tên</label>
                    <input type="text" class="form-control" name="last_name" value="${user?.last_name || ''}" required>
                </div>

                <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input type="email" class="form-control" name="email" value="${user?.email || ''}" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Số điện thoại</label>
                    <input type="text" class="form-control" name="phone_number" value="${user?.phone_number || ''}">
                </div>

                <div class="col-md-6">
                    <label class="form-label">Sinh nhật</label>
                    <input type="date" class="form-control" name="date_of_birth" value="${user?.date_of_birth || ''}">
                </div>
                <div class="col-md-6">
                    <label class="form-label">Địa chỉ</label>
                    <textarea class="form-control" name="address" rows="2">${user?.address || ''}</textarea>
                </div>

                <div class="col-12">
                    <label class="form-label">Ảnh đại diện</label>
                    ${user?.profile_picture ? `<div class="mb-2"><img src="${user.profile_picture}" class="rounded-circle" width="60" height="60"></div>` : ''}
                    <input type="file" class="form-control" name="profile_picture" accept="image/*">
                </div>

                ${!user ? `
                    <div class="col-md-6">
                    <label class="form-label">Mật khẩu</label>
                    <input type="password" class="form-control" name="password" required>
                    </div>
                    <div class="col-md-6">
                    <label class="form-label">Xác nhận mật khẩu</label>
                    <input type="password" class="form-control" name="password2" required>
                    </div>
                ` : ''}

                </div>

                <div class="d-flex justify-content-end mt-4">
                <button type="submit" class="btn btn-success me-2">${user ? 'Cập nhật' : 'Tạo mới'}</button>
                <button type="button" class="btn btn-secondary" id="cancel-user-form-2">Hủy</button>
                </div>
            </form>
            </div>
        </div>
        </div>
    `;

    const cancelForm = () => container.innerHTML = '';
    document.getElementById('cancel-user-form').onclick = cancelForm;
    document.getElementById('cancel-user-form-2').onclick = cancelForm;

    document.getElementById('user-form').onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        try {
        if (user) {
            await updateUser(user.id, formData);
            showAlert('success', 'Cập nhật thành công');
        } else {
            await createUser(formData);
            showAlert('success', 'Tạo người dùng thành công');
        }
        cancelForm();
        await renderUserList(root);
        } catch (err) {
        const message = err?.response?.data?.errors || err?.message || 'Lỗi không xác định';
        showAlert('error', Array.isArray(message) ? message.join(', ') : message);
        }
    };
}


async function handleEditUser(userId, root) {
  try {
    const users = await fetchAllUsers();
    const user = users.find(u => u.id == userId);
    if (!user) throw new Error('Không tìm thấy người dùng');
    renderUserForm(user, root);
  } catch (err) {
    showAlert('error', err.message || 'Lỗi khi tải người dùng');
  }
}

async function handleDeleteUser(userId, root) {
  if (!confirm('Bạn có chắc muốn xóa người dùng này?')) return;

  try {
    await deleteUser(userId);  
    showAlert('success', 'Xóa người dùng thành công');
    await renderUserList(root);
  } catch (err) {
    console.error('❌ Lỗi khi gọi deleteUser:', err);
    showAlert('error', err.message || 'Không thể xóa người dùng');
  }
}
