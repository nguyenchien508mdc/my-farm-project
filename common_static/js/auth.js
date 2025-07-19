// common_static\js\auth.js

// =============================
// Token Access/Storage Utils
// =============================

// Lấy access token từ localStorage
export function getAccessToken() {
  return localStorage.getItem('access_token');
}

// Lưu access token vào localStorage
export function setAccessToken(token) {
  localStorage.setItem('access_token', token);
}

// Xoá access token khi logout
export function clearToken() {
  localStorage.removeItem('access_token');
}

// Tạo header Authorization nếu có token
export function authHeaders() {
  const token = getAccessToken();
  return token ? { Authorization: 'Bearer ' + token } : {};
}

// =============================
// JWT Decode & Expiry Check
// =============================

function base64UrlDecode(str) {
  // Thay thế ký tự base64url về base64 chuẩn
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  // Thêm padding '=' nếu cần
  while (str.length % 4) {
    str += '=';
  }
  return atob(str);
}

export function parseJwt(token) {
  try {
    if (!token) return null;
    const base64Payload = token.split('.')[1];
    if (!base64Payload) return null;
    const payload = base64UrlDecode(base64Payload);
    return JSON.parse(payload);
  } catch (e) {
    return null;
  }
}


export function isTokenExpired(token) {
  const payload = parseJwt(token);
  if (!payload || !payload.exp) return true;
  const now = Math.floor(Date.now() / 1000);
  return payload.exp < now;
}

// =============================
// Refresh Access Token via Cookie
// =============================

export async function refreshAccessToken() {
  try {
    const res = await fetch('/api/core/token/refresh/', {
      method: 'POST',
      credentials: 'include', // để gửi cookie HttpOnly refresh token
    });
    if (!res.ok) {
        if (res.status === 401) {
            // Token không hợp lệ hoặc hết hạn, logout
            clearToken();
            window.location.href = '/login';
            return null;
        }
        // Có thể throw lỗi hoặc xử lý khác cho các status khác
        const errorText = await res.text();
        throw new Error(errorText || 'Lỗi khi gọi API');
    }
    const data = await res.json();
    if (data.access) {
      setAccessToken(data.access);
      return data.access;
    }
    return null;
  } catch (err) {
    console.error('Lỗi khi refresh token:', err);
    return null;
  }
}

// =============================
// Tự động fetch với refresh token
// =============================

export async function fetchWithAuth(url, options = {}) {
  try {
    let token = getAccessToken();

    if (!token) {
        // Không có token => chắc chắn chưa đăng nhập hoặc đã logout
        clearToken();
        window.location.href = '/login';
        return null;
    }

    if (isTokenExpired(token)) {
    // Có token nhưng hết hạn => thử refresh
        token = await refreshAccessToken();
        if (!token) {
            clearToken();
            window.location.href = '/login';
            return null;
        }
    }

    const res = await fetch(url, {
      ...options,
      headers: { ...options.headers, Authorization: 'Bearer ' + token },
      credentials: 'include', // để gửi cookie HttpOnly refresh token
    });
    if (res.status === 401) {
      clearToken();
      window.location.href = '/login';
      return null;
    }
    return res;
  } catch (err) {
    console.error('Lỗi fetchWithAuth:', err);
    clearToken();
    window.location.href = '/login';
    return null;
  }
}

export async function logout() {
  try {
    // Gửi yêu cầu logout để server xóa cookie refresh token
    await fetch('/api/core/logout/', {
      method: 'POST',
      credentials: 'include',
    });
  } catch (err) {
    console.error('Lỗi khi gọi logout API:', err);
  } finally {
    clearToken();
    window.location.href = '/';
  }
}

export async function fetchWithAuthOrRedirect(url, options = {}) {
  const currentPath = window.location.pathname;
  const response = await fetchWithAuth(url, options);

  if (!response || !response.ok) {
    window.location.href = `/login?next=${encodeURIComponent(currentPath)}`;
    return null;
  }

  return response;
}