import { fetchWithAuth } from '/static/js/auth.js';

// Lấy danh sách tất cả tài liệu của một farm theo farmId
export async function fetchFarmDocuments(farmId) {
  try {
    const response = await fetchWithAuth(`/api/farm/farms/${farmId}/documents/`);
    if (!response.ok) throw response;
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Lỗi khi lấy danh sách tài liệu:', error);
    throw error;
  }
}

// Lấy chi tiết tài liệu theo ID 
export async function fetchFarmDocumentDetail(documentId) {
  try {
    const response = await fetchWithAuth(`/api/farm/documents/${documentId}/`);
    if (!response.ok) throw response;
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết tài liệu:', error);
    throw error;
  }
}

// Tạo mới hoặc cập nhật tài liệu dùng farmId
export async function createOrUpdateFarmDocument(farmId, documentId, formData) {
  const url = documentId
    ? `/api/farm/documents/${documentId}/`
    : `/api/farm/documents/`;

  const method = documentId ? 'PATCH' : 'POST';

  try {
    const response = await fetchWithAuth(url, {
      method,
      body: formData,
    });
    if (!response.ok) throw response;
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Lỗi khi tạo/cập nhật tài liệu:', error);
    throw error;
  }
}

// Xóa tài liệu theo ID
export async function deleteFarmDocument(documentId) {
  try {
    const response = await fetchWithAuth(`/api/farm/documents/${documentId}/`, {
      method: 'DELETE',
    });
    if (!response.ok) throw response;
    return;
  } catch (error) {
    console.error('Lỗi khi xóa tài liệu:', error);
    throw error;
  }
}
