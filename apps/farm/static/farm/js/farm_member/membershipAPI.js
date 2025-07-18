// apps\farm\static\js\membershipAPI.js
import { authHeaders } from '/static/js/auth.js';

// Lấy danh sách tất cả membership của một farm theo farmId
export function fetchMemberships(farmId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/farms/${farmId}/memberships/`,
        type: 'GET',
        dataType: 'json',
        headers: authHeaders(),
        success: onSuccess,
        error: function(xhr, status, error) {
            console.error('Lỗi khi lấy danh sách membership:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Lấy chi tiết membership theo ID (pk) và farmId
export function fetchMembershipDetail(membershipId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/memberships/${membershipId}/`,
        type: 'GET',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi lấy chi tiết membership:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Tạo mới hoặc cập nhật membership (theo ID) dùng farmId
export function createOrUpdateMembership(farmId, membershipId, data, onSuccess, onError) {
    if (!membershipId && !data.farm) {
        data.farm = farmId;  // đảm bảo gửi farmId khi tạo mới
    }
    const url = membershipId
        ? `/api/farm/memberships/${membershipId}/`  // update
        : `/api/farm/memberships/`; // create

    const method = membershipId ? 'PATCH' : 'POST';

    $.ajax({
        url: url,
        type: method,
        headers: {
            ...authHeaders(),
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi tạo/cập nhật membership:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}

// Xóa membership theo ID dùng farmId
export function deleteMembership(membershipId, onSuccess, onError) {
    $.ajax({
        url: `/api/farm/memberships/${membershipId}/`,
        type: 'DELETE',
        headers: authHeaders(),
        success: onSuccess,
        error: function (xhr, status, error) {
            console.error('Lỗi khi xóa membership:', error);
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}