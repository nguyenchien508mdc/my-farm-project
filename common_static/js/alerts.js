// common_static\js\alerts.js

// Thêm CSS vào trang (chỉ chạy 1 lần)
(function addAlertStyles() {
  if (document.getElementById('custom-alert-styles')) return;
  const style = document.createElement('style');
  style.id = 'custom-alert-styles';
  style.textContent = `
    #alert-container {
      position: fixed;
      bottom: 1rem;
      right: 1rem;
      z-index: 1050;
      display: flex;
      flex-direction: column-reverse;
      gap: 0.5rem;
      max-width: 320px;
    }
    .custom-alert {
      pointer-events: auto;
      width: 320px;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      font-size: 14px;
      user-select: none;
      overflow: hidden;
      cursor: default;
      color: white;
      display: flex;
      flex-direction: column;
      animation-duration: 0.5s;
    }
    .custom-alert.bg-success { background-color: #28a745; }
    .custom-alert.bg-danger { background-color: #dc3545; }
    .custom-alert.bg-warning { background-color: #ffc107; color: #212529; }
    .custom-alert.bg-info { background-color: #17a2b8; }
    .custom-alert.bg-secondary { background-color: #6c757d; }

    .custom-alert .alert-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .custom-alert i {
      margin-right: 8px;
      font-style: normal;
      font-weight: bold;
      font-size: 18px;
      line-height: 1;
      user-select: none;
    }
    .btn-close {
      background: transparent;
      border: none;
      font-size: 18px;
      line-height: 1;
      opacity: 0.8;
      transition: opacity 0.3s ease;
      cursor: pointer;
      color: inherit;
    }
    .btn-close:hover {
      opacity: 1;
    }
    .alert-progress {
      height: 4px;
      background: rgba(255,255,255,0.3);
      border-radius: 4px;
      overflow: hidden;
      margin-top: 8px;
    }
    .alert-progress-bar {
      height: 100%;
      background-color: rgba(255,255,255,0.7);
      width: 100%;
      animation-name: progressbar;
      animation-timing-function: linear;
      animation-fill-mode: forwards;
    }
    @keyframes progressbar {
      from { width: 100%; }
      to { width: 0; }
    }
    /* Animation classes nếu dùng animate.css, nếu không thì bỏ */
    .animate__animated { animation-duration: 0.5s; animation-fill-mode: both; }
    .animate__fadeInRight { animation-name: fadeInRight; }
    .animate__fadeOutRight { animation-name: fadeOutRight; }
    @keyframes fadeInRight {
      from {
        opacity: 0;
        transform: translate3d(100%, 0, 0);
      }
      to {
        opacity: 1;
        transform: none;
      }
    }
    @keyframes fadeOutRight {
      from {
        opacity: 1;
        transform: none;
      }
      to {
        opacity: 0;
        transform: translate3d(100%, 0, 0);
      }
    }
  `;
  document.head.appendChild(style);

  // Tạo container alert nếu chưa có
  if (!document.getElementById('alert-container')) {
    const container = document.createElement('div');
    container.id = 'alert-container';
    document.body.appendChild(container);
  }
})();


export function showAlert(type, message, timeout = 5000) {
  const typeMap = {
    success: { class: 'bg-success', icon: '✔️' },
    error:   { class: 'bg-danger',  icon: '❌' },
    warning: { class: 'bg-warning', icon: '⚠️' },
    info:    { class: 'bg-info',    icon: 'ℹ️' },
  };

  const alertInfo = typeMap[type] || { class: 'bg-secondary', icon: '🔔' };
  const id = `alert-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

  const alertHtml = `
    <div id="${id}" class="custom-alert animate__animated animate__fadeInRight ${alertInfo.class}" tabindex="0">
      <div class="alert-header">
        <div><span>${alertInfo.icon}</span> ${message}</div>
        <button type="button" class="btn-close" aria-label="Close">&times;</button>
      </div>
      <div class="alert-progress">
        <div class="alert-progress-bar" style="animation-duration: ${timeout}ms;"></div>
      </div>
    </div>
  `;

  const container = document.getElementById('alert-container');
  container.insertAdjacentHTML('beforeend', alertHtml);
  const alertEl = document.getElementById(id);

  // Tự động ẩn alert
  setTimeout(() => {
    alertEl.classList.remove('animate__fadeInRight');
    alertEl.classList.add('animate__fadeOutRight');
    setTimeout(() => alertEl.remove(), 600);
  }, timeout);

  // Xử lý nút đóng
  alertEl.querySelector('.btn-close').addEventListener('click', () => {
    alertEl.remove();
  });
}
