import { fetchWithAuth, fetchWithAuthOrRedirect } from '/static/js/auth.js';

// Lấy danh sách tất cả người dùng (is_active=True)
export async function fetchAllUsers() {
    const res = await fetchWithAuthOrRedirect('/api/core/users/', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res || !res.ok) throw new Error('Lấy danh sách người dùng thất bại');
    return await res.json();
}

// Gọi API: thêm người dùng
export async function createUser(data) {
    const res = await fetchWithAuth('/api/core/users/', {
      method: 'POST',
      body: data,
    });
    if (!res.ok) throw new Error('Thêm người dùng thất bại');
    return res.json();
}

// Gọi API: sửa người dùng
export async function updateUser(id, data) {
    let options = {
      method: 'PATCH',
      headers: {},
      body: null,
    };

    if (data instanceof FormData) {
      options.body = data;
    } else {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(data);
    }

    const res = await fetchWithAuth(`/api/core/users/${id}/`, options);
    if (!res.ok) throw new Error('Cập nhật người dùng thất bại');
    return res.json();
}

// Gọi API: xóa người dùng
export async function deleteUser(id) {
  const res = await fetchWithAuth(`/api/core/users/${id}/delete/`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error('❌ Xóa thất bại:', res.status, errorText);
    throw new Error('Xóa người dùng thất bại');
  }
}


// Lấy danh sách người dùng chưa thuộc farmexport async function fetchFreeUsers(farmId) {
export async function fetchFreeUsers(farmId) {
    const res = await fetchWithAuth(`/api/core/free-users/${farmId}/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res || !res.ok) throw new Error('Lấy danh sách người dùng chưa thuộc farm thất bại');
    const data = await res.json();
    console.log('Free users data:', data);  // <-- Thêm dòng này để xem dữ liệu
    return data;
}


// Lấy thông tin người dùng hiện tại (me)
export async function fetchCurrentUser() {
    const res = await fetchWithAuth('/api/core/me/', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res || !res.ok) throw new Error('Lấy thông tin người dùng thất bại');
    return await res.json();
}
