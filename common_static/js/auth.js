
// =============================
// Refresh Access Token via Cookie
// =============================

export async function refreshAccessToken() {
  try {
    const res = await fetch('/api/core/token/refresh/', {
      method: 'POST',
      credentials: 'include', // để gửi cookie refresh_token
    });

    if (!res.ok) {
      if (res.status === 401 || res.status === 403) {
        // Refresh token hết hạn hoặc không hợp lệ
        return null;
      }
      const errorText = await res.text();
      throw new Error(errorText || 'Lỗi khi gọi API refresh');
    }

    // Access token mới sẽ được set lại vào cookie HttpOnly từ backend
    return true;
  } catch (err) {
    console.error('Lỗi khi refresh token:', err);
    return null;
  }
}

// =============================
// Tự động fetch với refresh nếu cần
// =============================

export async function fetchWithAuth(url, options = {}, retry = true) {
  try {
    let res = await fetch(url, {
      ...options,
      credentials: 'include',
    });

    if ((res.status === 401 || res.status === 403) && retry) {
      // Nếu đang refresh, đợi
      if (isRefreshing) {
        await refreshPromise;
      } else {
        isRefreshing = true;
        refreshPromise = refreshAccessToken()
          .then((success) => {
            if (!success) throw new Error("Refresh failed");
          })
          .finally(() => {
            isRefreshing = false;
            refreshPromise = null;
          });

        try {
          await refreshPromise;
        } catch (err) {
          console.warn('❌ Refresh token thất bại khi đang chờ');
          return null;
        }
      }

      // Sau khi refresh → thử lại request 1 lần duy nhất
      return await fetchWithAuth(url, options, false);
    }

    return res;
  } catch (err) {
    console.error('Lỗi fetchWithAuth:', err);
    return null;
  }
}


// =============================
// Logout: gọi API để xóa cookie
// =============================

export async function logout() {
  try {
    await fetch('/api/core/logout/', {
      method: 'POST',
      credentials: 'include',
    });
  } catch (err) {
    console.error('Lỗi khi gọi logout API:', err);
  } finally {
    window.location.href = '/';
  }
}

// =============================
// Fetch có redirect nếu lỗi auth
// =============================

export async function fetchWithAuthOrRedirect(url, options = {}) {
  const currentPath = window.location.pathname;
  const response = await fetchWithAuth(url, options);

  if (!response || !response.ok) {
    window.location.href = `/login?next=${encodeURIComponent(currentPath)}`;
    return null;
  }

  return response;
}

// =============================
// Auto Refresh Access Token Định Kỳ
// =============================

let refreshIntervalId = null;

export function setupAutoRefresh(intervalMinutes = 22) {
  // 🧹 Dọn timer cũ nếu đã có
  if (refreshIntervalId) {
    clearInterval(refreshIntervalId);
  }

  // ⏰ Tạo mới
  refreshIntervalId = setInterval(async () => {
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      console.warn('⚠️ Token refresh thất bại, có thể đã hết hạn.');
      logout(); // Gọi logout nếu refresh thất bại
    } else {
      console.log('🔁 Access token được làm mới thành công');
    }
  }, intervalMinutes * 60 * 1000);
}
