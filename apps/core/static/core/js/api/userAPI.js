// apps\core\static\js\userAPI.js

import { authHeaders } from '/static/js/auth.js';

// Lấy danh sách tất cả người dùng (is_active=True)
export function fetchAllUsers(onSuccess, onError) {
    $.ajax({
        url: '/api/core/users/',
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        success: onSuccess,
        error: onError
    });
}

// Lấy danh sách người dùng chưa thuộc farm
export function fetchFreeUsers(farmId, onSuccess, onError) {
    $.ajax({
        url: `/api/core/free-users/${farmId}/`,
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        timeout: 5000,
        success: onSuccess,
        error: onError
    });
}

// Lấy thông tin người dùng hiện tại (me)
export function fetchCurrentUser(onSuccess, onError) {
    $.ajax({
        url: '/api/core/me/',
        type: 'GET',
        headers: authHeaders(),
        dataType: 'json',
        success: onSuccess,
        error: onError
    });
}

// Đăng ký người dùng mới
export function registerUser(userData, onSuccess, onError) {
    $.ajax({
        url: '/api/core/register/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(userData),
        success: onSuccess,
        error: onError
    });
}

// Cập nhật thông tin người dùng hiện tại
export function updateCurrentUser(userData, onSuccess, onError) {
    $.ajax({
        url: '/api/core/me/update/',
        type: 'PATCH',
        headers: {
            ...authHeaders(),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(userData),
        success: onSuccess,
        error: onError
    });
}

// Đổi mật khẩu người dùng hiện tại
export function changePassword(data, onSuccess, onError) {
    $.ajax({
        url: '/api/core/me/change-password/',
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
