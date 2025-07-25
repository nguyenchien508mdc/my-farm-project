import { fetchWithAuth, fetchWithAuthOrRedirect } from '/static/js/auth.js';

// Lấy danh sách farm
export async function fetchFarmList() {
  const response = await fetchWithAuthOrRedirect('/api/farm/farms/');
  if (!response.ok) throw new Error('Lỗi khi gọi danh sách farm');
  return response.json();
}

// Lấy chi tiết farm theo id (dùng khi edit form)
export async function fetchFarmDetail(farmId) {
  const response = await fetchWithAuth(`/api/farm/farms/${farmId}/`);
  if (!response.ok) throw new Error('Lỗi khi lấy chi tiết farm');
  return response.json();
}

// Tạo hoặc cập nhật farm
export async function createOrUpdateFarm(farmId, dataObj) {
  const url = farmId ? `/api/farm/farms/${farmId}/` : '/api/farm/farms/';
  const method = farmId ? 'PATCH' : 'POST';

  const response = await fetchWithAuth(url, {
    method,
    body: dataObj,  
  });

  if (!response.ok) throw new Error('Lỗi khi tạo/cập nhật farm');
  return response.json();
}

// Xóa farm
export async function deleteFarm(farmId) {
  const response = await fetchWithAuth(`/api/farm/farms/${farmId}/`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Lỗi khi xóa farm');
  // Không cần trả về gì, chỉ thành công
}
