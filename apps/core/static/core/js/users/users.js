// apps\core\static\js\users\users.js

import { fetchAllUsers  } from '/static/js/userAPI.js';

// Tự động chạy khi DOM load xong
document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.querySelector('#user-table tbody');
    if (!tbody) return;

    fetchAllUsers((users) => {
        tbody.innerHTML = ''; // Xóa dữ liệu cũ nếu có
        users.forEach(user => {
            const row = `
                <tr>
                    <td>${user.first_name} ${user.last_name}</td>
                    <td>${user.email}</td>
                    <td>${user.username}</td>
                </tr>`;
            tbody.innerHTML += row;
        });
    }, (xhr, status, error) => {
        alert('Không tải được danh sách người dùng.');
    });
});
