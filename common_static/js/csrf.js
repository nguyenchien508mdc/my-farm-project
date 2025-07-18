// common_static\js\csrf.js

// Hàm lấy giá trị cookie theo tên
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Kiểm tra cookie bắt đầu bằng tên cần tìm
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Hàm lấy CSRF token
export function getCSRFToken() {
    return getCookie('csrftoken');
}
