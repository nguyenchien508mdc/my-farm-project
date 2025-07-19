export function renderAdminSidebar() {
  return `
    <div class="position-sticky pt-3" style="top: 70px; height: calc(100vh - 70px); overflow-y: auto; padding: 0 1rem 1rem 1rem; background: #fff; box-shadow: 0 0 12px rgb(0 0 0 / 0.1); border-radius: 0.5rem;">

      <div class="mb-3">
        <a href="#" class="d-flex align-items-center text-decoration-none text-primary fw-semibold p-3 rounded shadow-sm" style="border: 1px solid #0d6efd;">
          <i class="fa-solid fa-gauge-high me-3 fs-5"></i>
          <span>Bảng điều khiển</span>
        </a>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownFarm" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-tractor me-3 fs-5 text-success"></i>
            <span>Quản lý Nông trại</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownFarm" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="/password-change/" data-link>Thông tin nông trại</a></li>
          <li><a class="dropdown-item text-secondary" href="/farm/" data-link>Thành viên</a></li>
          <li><a class="dropdown-item text-secondary" href="/farm/" data-link>Tài liệu</a></li>
        </ul>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownCrop" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-seedling me-3 fs-5 text-success"></i>
            <span>Quản lý Cây trồng</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownCrop" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="#">Loại cây trồng</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Danh sách cây trồng</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Giai đoạn phát triển</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Thu hoạch</a></li>
        </ul>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownLivestock" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-cow me-3 fs-5 text-warning"></i>
            <span>Quản lý Vật nuôi</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownLivestock" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="#">Loại vật nuôi</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Giống vật nuôi</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Danh sách vật nuôi</a></li>
        </ul>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownOperation" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-list-check me-3 fs-5 text-info"></i>
            <span>Hoạt động</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownOperation" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="#">Công việc</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Tưới tiêu</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Bón phân</a></li>
        </ul>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownInventory" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-warehouse me-3 fs-5 text-secondary"></i>
            <span>Quản lý Kho</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownInventory" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="#">Nhà cung cấp</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Danh mục vật tư</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Vật tư tồn kho</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Nhập/Xuất kho</a></li>
        </ul>
      </div>

      <div class="dropdown mb-2">
        <a href="#" class="d-flex align-items-center justify-content-between text-decoration-none text-dark fw-semibold p-3 rounded border shadow-sm dropdown-toggle" 
           id="dropdownSales" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
          <span class="d-flex align-items-center">
            <i class="fa-solid fa-cart-shopping me-3 fs-5 text-danger"></i>
            <span>Bán hàng</span>
          </span>
        </a>
        <ul class="dropdown-menu ps-4" aria-labelledby="dropdownSales" style="border:none;">
          <li><a class="dropdown-item text-secondary" href="#">Danh mục sản phẩm</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Sản phẩm</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Đơn hàng</a></li>
          <li><a class="dropdown-item text-secondary" href="#">Khuyến mãi</a></li>
        </ul>
      </div>

      <div class="mt-3">
        <a href="#" class="d-flex align-items-center text-decoration-none text-primary fw-semibold p-3 rounded shadow-sm border" style="background-color: #f8f9fa;">
          <i class="fa-solid fa-chart-pie me-3 fs-5"></i>
          <span>Báo cáo & Phân tích</span>
        </a>
      </div>

    </div>
  `;
}
