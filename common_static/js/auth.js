// common_static\js\auth.js

// Lấy access token từ localStorage
export function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Tạo header Authorization nếu có token
export function authHeaders() {
    const token = getAccessToken();
    return token ? { 'Authorization': 'Bearer ' + token } : {};
}

export function parseJwt (token) {
    var base64Payload = token.split('.')[1];
    var payload = atob(base64Payload); 
    return JSON.parse(payload);
}