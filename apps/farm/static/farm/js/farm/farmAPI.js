// apps/farm/static/js/farmAPI.js

import { authHeaders } from '/static/js/auth.js';

// Lấy danh sách farm
export function fetchFarmList(onSuccess, onError) {
    $.ajax({
        url: '/api/farm/farms/',
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi gọi danh sách farm:', error);
            if (typeof onError === 'function') onError(xhr, status, error);
        }
    });
}

// Dùng khi edit form
export function fetchFarmDetail(farmId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/farms/${farmId}/`,
        type: 'GET',
        headers: authHeaders(),  
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi lấy chi tiết farm:', error);
            if (typeof onError === 'function') onError(xhr, status, error);
        }
    });
}

// Tạo hoặc cập nhật farm
export function createOrUpdateFarm(farmId, formData, onSuccess, onError) {
    const url = farmId ? `/api/farm/farms/${farmId}/` : '/api/farm/farms/';
    const method = farmId ? 'PATCH' : 'POST';
    $.ajax({
        url: url,
        type: method,
        headers: {
            ...authHeaders()
        },
        data: formData,
        processData: false,
        contentType: false,
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi tạo/cập nhật farm:', error);
            if (typeof onError === 'function') onError(xhr, status, error);
        }
    });
}

// Xóa farm
export function deleteFarm(farmId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/farms/${farmId}/`,
        type: 'DELETE',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi xóa farm:', error);
            console.log('Response:', xhr.responseText);
            if (typeof onError === 'function') onError(xhr, status, error);
        }
    });
}


