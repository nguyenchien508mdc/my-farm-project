// apps/farm/static/js/farmDocumentAPI.js
import { authHeaders } from '/static/js/auth.js';

// Lấy danh sách tất cả tài liệu của một farm theo farmId
export function fetchFarmDocuments(farmId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/farms/${farmId}/documents/`,
        type: 'GET',
        dataType: 'json',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi lấy danh sách tài liệu:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Lấy chi tiết tài liệu theo ID 
export function fetchFarmDocumentDetail(documentId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/documents/${documentId}/`,
        type: 'GET',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi lấy chi tiết tài liệu:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Tạo mới hoặc cập nhật tài liệu dùng farmId
export function createOrUpdateFarmDocument(farmId, documentId, formData, onSuccess, onError) {
    if (!documentId && !formData.has('farm')) {
        formData.append('farm', farmId);
    }
    const url = documentId
        ? `/api/farm/documents/${documentId}/`
        : `/api/farm/documents/`;

    const method = documentId ? 'PATCH' : 'POST';

    $.ajax({
        url: url,
        type: method,
        headers: authHeaders(),
        data: formData,
        processData: false,
        contentType: false,
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi tạo/cập nhật tài liệu:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Xóa tài liệu theo ID dùng farmId
export function deleteFarmDocument( documentId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/documents/${documentId}/`,
        type: 'DELETE',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi xóa tài liệu:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}
