import { renderFooter } from './footer_render.js';

document.addEventListener('DOMContentLoaded', () => {
  const footerRoot = document.getElementById('footer-root');
  if (footerRoot) {
    footerRoot.innerHTML = renderFooter();
  } else {
    console.warn('Không tìm thấy phần tử #footer-root để render footer.');
  }
});
