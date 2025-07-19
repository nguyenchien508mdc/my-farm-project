// apps/farm/static/js/farmAPI.js

import { fetchWithAuth, fetchWithAuthOrRedirect } from '/static/js/auth.js';

// Lấy danh sách farm
export async function fetchFarmList(onSuccess, onError) {
  try {
    const response = await fetchWithAuthOrRedirect('/api/farm/farms/');
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi gọi danh sách farm:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Lấy chi tiết farm theo id (dùng khi edit form)
export async function fetchFarmDetail(farmId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/farms/${farmId}/`);
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết farm:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Tạo hoặc cập nhật farm
export async function createOrUpdateFarm(farmId, formData, onSuccess, onError) {
  const url = farmId ? `/api/farm/farms/${farmId}/` : '/api/farm/farms/';
  const method = farmId ? 'PATCH' : 'POST';

  try {
    const response = await fetchWithAuth(url, {
      method,
      body: formData,
    });
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi tạo/cập nhật farm:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Xóa farm
export async function deleteFarm(farmId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/farms/${farmId}/`, {
      method: 'DELETE',
    });
    if (!response.ok) throw response;
    onSuccess();
  } catch (error) {
    console.error('Lỗi khi xóa farm:', error);
    if (typeof onError === 'function') onError(error);
  }
}


