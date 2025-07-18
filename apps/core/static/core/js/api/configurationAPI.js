// apps\core\static\js\configurationAPI.js
import { authHeaders } from '/static/js/auth.js';

// Lấy danh sách tất cả cấu hình
export function fetchConfigurations(onSuccess, onError) {
    $.ajax({
        url: '/api/core/configurations/',
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        success: onSuccess,
        error: onError
    });
}

// Lấy chi tiết một cấu hình theo ID
export function fetchConfigurationDetail(id, onSuccess, onError) {
    $.ajax({
        url: `/api/core/configurations/${id}/`,
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        success: onSuccess,
        error: onError
    });
}

// Tạo mới một cấu hình
export function createConfiguration(data, onSuccess, onError) {
    $.ajax({
        url: '/api/core/configurations/',
        type: 'POST',
        headers: {
            ...authHeaders(),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),
        success: onSuccess,
        error: onError
    });
}

// Cập nhật một cấu hình theo ID
export function updateConfiguration(id, data, onSuccess, onError) {
    $.ajax({
        url: `/api/core/configurations/${id}/`,
        type: 'PATCH',
        headers: {
            ...authHeaders(),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),
        success: onSuccess,
        error: onError
    });
}

// Xóa một cấu hình theo ID
export function deleteConfiguration(id, onSuccess, onError) {
    $.ajax({
        url: `/api/core/configurations/${id}/`,
        type: 'DELETE',
        headers: authHeaders(),
        success: onSuccess,
        error: onError
    });
}
