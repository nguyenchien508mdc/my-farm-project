import { fetchWithAuth } from '/static/js/auth.js';

// Lấy danh sách tất cả cấu hình
export async function fetchConfigurations() {
  const res = await fetchWithAuth('/api/core/configurations/', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res || !res.ok) throw new Error('Lỗi khi lấy danh sách cấu hình');
  return await res.json();
}

// Lấy chi tiết một cấu hình theo ID
export async function fetchConfigurationDetail(id) {
  const res = await fetchWithAuth(`/api/core/configurations/${id}/`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res || !res.ok) throw new Error(`Lỗi khi lấy cấu hình ID ${id}`);
  return await res.json();
}

// Tạo mới một cấu hình
export async function createConfiguration(data) {
  const res = await fetchWithAuth('/api/core/configurations/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    let errorData = {};
    try {
      errorData = await res.json();
    } catch {}
    throw new Error(errorData.detail || 'Lỗi khi tạo mới cấu hình');
  }
  return await res.json();
}

// Cập nhật một cấu hình theo ID
export async function updateConfiguration(id, data) {
  const res = await fetchWithAuth(`/api/core/configurations/${id}/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    let errorData = {};
    try {
      errorData = await res.json();
    } catch {}
    throw new Error(errorData.detail || `Lỗi khi cập nhật cấu hình ID ${id}`);
  }
  return await res.json();
}

// Xóa một cấu hình theo ID
export async function deleteConfiguration(id) {
  const res = await fetchWithAuth(`/api/core/configurations/${id}/`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) {
    let errorData = {};
    try {
      errorData = await res.json();
    } catch {}
    throw new Error(errorData.detail || `Lỗi khi xóa cấu hình ID ${id}`);
  }
  return true;
}
