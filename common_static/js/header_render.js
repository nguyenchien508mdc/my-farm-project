// header_render.js

export function renderHeader(user) {
  const isAuthenticated = user?.isAuthenticated;
  const username = user?.username || '';
  const role = user?.role || '';

  return `
  <nav class="navbar navbar-expand-md navbar-dark bg-success sticky-top py-2 px-3">
    <div class="container-fluid">
      <!-- Logo và tên nông trại bên trái -->
      <div class="d-flex align-items-center">
        <i class="fa fa-leaf fa-2x text-white me-2"></i>
        <a class="navbar-brand fw-bold m-0" href="#" style="cursor: pointer;">
          NÔNG TRẠI ${isAuthenticated ? `${username} - ${role}` : ''}
        </a>
      </div>

      <!-- Nút toggle cho mobile -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain"
        aria-controls="navbarMain" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Các menu điều hướng bên phải -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarMain">
        <ul class="navbar-nav">
          <li class="nav-item mx-1">
            <a class="nav-link px-3 py-2 d-flex align-items-center" href="/" data-link>
              <i class="fa fa-home me-1"></i>
              <span>Trang chủ</span>
            </a>
          </li>
          <li class="nav-item mx-1">
            <a class="nav-link px-3 py-2 d-flex align-items-center" href="#">
              <i class="fa fa-shopping-basket me-1"></i>
              <span>Sản phẩm</span>
            </a>
          </li>
          <li class="nav-item mx-1">
            <a class="nav-link px-3 py-2 d-flex align-items-center" href="#">
              <i class="fa fa-info-circle me-1"></i>
              <span>Giới thiệu</span>
            </a>
          </li>
          <li class="nav-item mx-1">
            <a class="nav-link px-3 py-2 d-flex align-items-center" href="#">
              <i class="fa fa-newspaper-o me-1"></i>
              <span>Tin tức</span>
            </a>
          </li>
          <li class="nav-item mx-1">
            <a class="nav-link px-3 py-2 d-flex align-items-center" href="#">
              <i class="fa fa-phone me-1"></i>
              <span>Liên hệ</span>
            </a>
          </li>

          <!-- Dropdown tài khoản -->
          <li class="nav-item dropdown ms-2">
            <a class="nav-link dropdown-toggle px-3 py-2 d-flex align-items-center" href="#" id="accountDropdown" role="button"
              data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
              <i class="fas fa-user-circle me-1"></i>
              <span>${isAuthenticated ? `${username} `: 'Tài khoản'}</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="accountDropdown">
              ${isAuthenticated
              ? `
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/profile/" data-link>
                    <i class="fas fa-user me-2"></i> Thông tin cá nhân
                  </a>
                </li>
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/profile-update/" data-link>
                    <i class="fas fa-user-edit me-2"></i> Cập nhật thông tin
                  </a>
                </li>
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/password-change/" data-link>
                    <i class="fas fa-key me-2"></i> Đổi mật khẩu
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <button id="logout-btn" class="dropdown-item d-flex align-items-center">
                    <i class="fas fa-sign-out-alt me-2"></i> Đăng xuất
                  </button>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/settings" data-link>
                    <i class="fas fa-cog me-2"></i> Cài đặt
                  </a>
                </li>
              `
              : `
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/login">
                    <i class="fas fa-sign-in me-2"></i> Đăng nhập
                  </a>
                </li>
                <li>
                  <a class="dropdown-item d-flex align-items-center" href="/register">
                    <i class="fas fa-user-plus me-2"></i> Đăng ký
                  </a>
                </li>
              `
            }
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  `;
}
