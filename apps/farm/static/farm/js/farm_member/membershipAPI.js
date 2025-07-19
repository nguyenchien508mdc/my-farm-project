// apps\farm\static\js\membershipAPI.js

import { fetchWithAuth } from '/static/js/auth.js';

// Lấy danh sách tất cả membership của một farm theo farmId
export async function fetchMemberships(farmId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/farms/${farmId}/memberships/`);
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi lấy danh sách membership:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Lấy chi tiết membership theo ID (pk)
export async function fetchMembershipDetail(membershipId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/memberships/${membershipId}/`);
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết membership:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Tạo mới hoặc cập nhật membership (theo ID) dùng farmId
export async function createOrUpdateMembership(farmId, membershipId, data, onSuccess, onError) {
  if (!membershipId && !data.farm) {
    data.farm = farmId;  // đảm bảo gửi farmId khi tạo mới
  }

  const url = membershipId
    ? `/api/farm/memberships/${membershipId}/`
    : `/api/farm/memberships/`;

  const method = membershipId ? 'PATCH' : 'POST';

  try {
    const response = await fetchWithAuth(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw response;
    const resData = await response.json();
    onSuccess(resData);
  } catch (error) {
    console.error('Lỗi khi tạo/cập nhật membership:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Xóa membership theo ID
export async function deleteMembership(membershipId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/memberships/${membershipId}/`, {
      method: 'DELETE',
    });
    if (!response.ok) throw response;
    onSuccess();
  } catch (error) {
    console.error('Lỗi khi xóa membership:', error);
    if (typeof onError === 'function') onError(error);
  }
}
