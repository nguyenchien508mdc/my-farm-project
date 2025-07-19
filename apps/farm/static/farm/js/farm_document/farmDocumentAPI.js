// apps/farm/static/js/farmDocumentAPI.js

import { fetchWithAuth } from '/static/js/auth.js';

// Lấy danh sách tất cả tài liệu của một farm theo farmId
export async function fetchFarmDocuments(farmId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/farms/${farmId}/documents/`);
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi lấy danh sách tài liệu:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Lấy chi tiết tài liệu theo ID 
export async function fetchFarmDocumentDetail(documentId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/documents/${documentId}/`);
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết tài liệu:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Tạo mới hoặc cập nhật tài liệu dùng farmId
export async function createOrUpdateFarmDocument(farmId, documentId, formData, onSuccess, onError) {
  if (!documentId && !formData.has('farm')) {
    formData.append('farm', farmId);
  }
  const url = documentId
    ? `/api/farm/documents/${documentId}/`
    : `/api/farm/documents/`;

  const method = documentId ? 'PATCH' : 'POST';

  try {
    const response = await fetchWithAuth(url, {
      method,
      body: formData,
      // Khi dùng FormData, không set Content-Type để browser tự xử lý
    });
    if (!response.ok) throw response;
    const data = await response.json();
    onSuccess(data);
  } catch (error) {
    console.error('Lỗi khi tạo/cập nhật tài liệu:', error);
    if (typeof onError === 'function') onError(error);
  }
}

// Xóa tài liệu theo ID
export async function deleteFarmDocument(documentId, onSuccess, onError) {
  try {
    const response = await fetchWithAuth(`/api/farm/documents/${documentId}/`, {
      method: 'DELETE',
    });
    if (!response.ok) throw response;
    onSuccess();
  } catch (error) {
    console.error('Lỗi khi xóa tài liệu:', error);
    if (typeof onError === 'function') onError(error);
  }
}
