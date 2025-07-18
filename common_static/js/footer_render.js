export function renderFooter() {
  return `
<footer class="bg-dark text-white pt-4 pb-2">
  <div class="container">
    <div class="row">
      <div class="col-md-4 mb-3">
        <h5><i class="fa fa-leaf"></i> Nông Trại Xanh</h5>
        <p class="text-muted">Ứng dụng công nghệ vào nông nghiệp để mang lại sản phẩm chất lượng cao.</p>
        <div class="social-icons">
          <a href="#" class="text-white me-2"><i class="fa fa-facebook"></i></a>
          <a href="#" class="text-white me-2"><i class="fa fa-twitter"></i></a>
          <a href="#" class="text-white me-2"><i class="fa fa-instagram"></i></a>
          <a href="#" class="text-white"><i class="fa fa-youtube"></i></a>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <h5>Liên kết nhanh</h5>
        <ul class="list-unstyled">
          <li><a href="#" class="text-muted">Trang chủ</a></li>
          <li><a href="#" class="text-muted">Sản phẩm</a></li>
          <li><a href="#" class="text-muted">Giới thiệu</a></li>
          <li><a href="#" class="text-muted">Tin tức</a></li>
          <li><a href="#" class="text-muted">Liên hệ</a></li>
        </ul>
      </div>

      <div class="col-md-4 mb-3">
        <h5>Liên hệ</h5>
        <ul class="list-unstyled text-muted">
          <li><i class="fa fa-map-marker"></i> 123 Đường Nông Thôn, Xã An Lạc</li>
          <li><i class="fa fa-phone"></i> (0123) 456 789</li>
          <li><i class="fa fa-envelope"></i> info@nongtraixanh.com</li>
        </ul>
      </div>
    </div>

    <hr class="my-3 bg-secondary">

    <div class="row">
      <div class="col-md-6 text-center text-md-start">
        <p class="mb-0">&copy; 2023 Nông Trại Xanh. All rights reserved.</p>
      </div>
      <div class="col-md-6 text-center text-md-end">
        <p class="mb-0">
          <a href="#" class="text-muted me-2">Điều khoản</a>
          <a href="#" class="text-muted">Chính sách bảo mật</a>
        </p>
      </div>
    </div>
  </div>
</footer>
`;
}
