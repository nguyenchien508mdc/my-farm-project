export function renderCustomerSidebar() {
  return `
    <div class="sidebar-sticky pt-2">
      <ul class="nav flex-column">
        <li class="nav-item">
          <a class="nav-link active" href="#">
            <i class="fa-solid fa-gauge-high me-2"></i>
            <span>Bảng điều khiển</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/orders">
            <i class="fa-solid fa-cart-shopping me-2"></i>
            <span>Đơn hàng</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/profile">
            <i class="fa-solid fa-user me-2"></i>
            <span>Hồ sơ cá nhân</span>
          </a>
        </li>
      </ul>
    </div>
  `;
}
