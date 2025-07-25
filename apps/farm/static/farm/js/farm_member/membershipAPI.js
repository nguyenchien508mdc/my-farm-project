import { fetchWithAuth } from '/static/js/auth.js';

// Lấy danh sách tất cả membership của một farm theo farmId
export async function fetchMemberships(farmId) {
  const response = await fetchWithAuth(`/api/farm/farms/${farmId}/memberships/`);
  if (!response.ok) throw response;
  return await response.json();
}

// Lấy chi tiết membership theo ID (pk)
export async function fetchMembershipDetail(membershipId) {
  const response = await fetchWithAuth(`/api/farm/memberships/${membershipId}/`);
  if (!response.ok) throw response;
  return await response.json();
}

// Tạo mới hoặc cập nhật membership (theo ID) dùng farmId
export async function createOrUpdateMembership(farmId, membershipId, data) {
  const url = membershipId
    ? `/api/farm/memberships/${membershipId}/`
    : `/api/farm/memberships/`;

  const method = membershipId ? 'PATCH' : 'POST';

  const response = await fetchWithAuth(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw response;
  return await response.json();
}

// Xóa membership theo ID
export async function deleteMembership(membershipId) {
  const response = await fetchWithAuth(`/api/farm/memberships/${membershipId}/`, {
    method: 'DELETE',
  });
  if (!response.ok) throw response;
  // Không cần return gì khi xóa thành công
}
