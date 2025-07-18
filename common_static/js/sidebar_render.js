export function renderSidebar() {
  return `
<div class="sidebar-sticky pt-2">
  <!-- Menu chính -->
  <ul class="nav flex-column">
      <li class="nav-item">
          <a class="nav-link active" href="#">
              <i class="fa-solid fa-gauge-high me-2"></i>
              <span>Bảng điều khiển</span>
          </a>
      </li>
      
      <!-- Quản lý nông trại -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="{% url 'farm:farm-list' %}">
              <i class="fa-solid fa-tractor me-2"></i>
              <span>Quản lý Nông trại</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse show" id="farmSubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="/password-change">Thông tin nông trại</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="/farm">Thành viên</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="/farm">Tài liệu</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Quản lý cây trồng -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#cropSubmenu">
              <i class="fa-solid fa-seedling me-2"></i>
              <span>Quản lý Cây trồng</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse" id="cropSubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="#">Loại cây trồng</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Danh sách cây trồng</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Giai đoạn phát triển</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Thu hoạch</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Quản lý vật nuôi -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#">
              <i class="fa-solid fa-cow me-2"></i>
              <span>Quản lý Vật nuôi</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse" id="livestockSubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="#">Loại vật nuôi</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Giống vật nuôi</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Danh sách vật nuôi</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Quản lý hoạt động -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#operationSubmenu">
              <i class="fa-solid fa-list-check me-2"></i>
              <span>Hoạt động</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse" id="operationSubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="#">Công việc</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Tưới tiêu</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Bón phân</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Quản lý kho -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#inventorySubmenu">
              <i class="fa-solid fa-warehouse me-2"></i>
              <span>Quản lý Kho</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse" id="inventorySubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="#">Nhà cung cấp</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Danh mục vật tư</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Vật tư tồn kho</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Nhập/Xuất kho</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Bán hàng -->
      <li class="nav-item">
          <a class="nav-link" data-bs-toggle="collapse" href="#salesSubmenu">
              <i class="fa-solid fa-cart-shopping me-2"></i>
              <span>Bán hàng</span>
              <i class="fa-solid fa-chevron-right ms-auto"></i>
          </a>
          <div class="collapse" id="salesSubmenu">
              <ul class="nav flex-column submenu ps-3">
                  <li class="nav-item">
                      <a class="nav-link" href="#">Danh mục sản phẩm</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Sản phẩm</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Đơn hàng</a>
                  </li>
                  <li class="nav-item">
                      <a class="nav-link" href="#">Khuyến mãi</a>
                  </li>
              </ul>
          </div>
      </li>
      
      <!-- Báo cáo & Phân tích -->
      <li class="nav-item">
          <a class="nav-link" href="#">
              <i class="fa-solid fa-chart-pie me-2"></i>
              <span>Báo cáo & Phân tích</span>
          </a>
      </li>
  </ul>
</div>

<style>
  /* Style cho sidebar */
  .sidebar-sticky {
      position: sticky;
      top: 70px;
      height: calc(100vh - 70px);
      overflow-y: auto;
      padding-bottom: 20px;
  }
  
  .nav-link {
      color: #333;
      padding: 10px 15px;
      border-radius: 4px;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      transition: all 0.2s;
  }
  
  .nav-link:hover, .nav-link.active {
      background-color: rgba(40, 167, 69, 0.1);
      color: #28a745;
  }
  
  .nav-link.active {
      font-weight: 600;
  }
  
  .submenu .nav-link {
      padding: 8px 15px;
      font-size: 0.9rem;
  }
  
  .fa-chevron-right {
      transition: transform 0.3s;
  }
  
  .nav-link[aria-expanded="true"] .fa-chevron-right {
      transform: rotate(90deg);
  }
  
  /* Scrollbar */
  .sidebar-sticky::-webkit-scrollbar {
      width: 5px;
  }
  
  .sidebar-sticky::-webkit-scrollbar-thumb {
      background: #ccc;
      border-radius: 4px;
  }
</style>
  `;
}
