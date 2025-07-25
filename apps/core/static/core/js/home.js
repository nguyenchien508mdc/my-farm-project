export async function createHomePage() {

    root.innerHTML = `
    <div class="container-fluid">
        <!-- Carousel -->
        <div id="farmCarousel" class="carousel slide mb-4 shadow" data-bs-ride="carousel">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#farmCarousel" data-bs-slide-to="0" class="active"></button>
                <button type="button" data-bs-target="#farmCarousel" data-bs-slide-to="1"></button>
                <button type="button" data-bs-target="#farmCarousel" data-bs-slide-to="2"></button>
            </div>
            <div class="carousel-inner rounded">
                <div class="carousel-item active">
                    <div style="width:100%; height:400px; background-color:#28a745;" class="d-block"></div>
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded">
                        <h5>Nông Sản Hữu Cơ</h5>
                        <p>Cam kết chất lượng không hóa chất độc hại</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <div style="width:100%; height:400px; background-color:#20c997;" class="d-block"></div>
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded">
                        <h5>Công Nghệ Nông Nghiệp 4.0</h5>
                        <p>Ứng dụng công nghệ cao vào sản xuất</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <div style="width:100%; height:400px; background-color:#17a2b8;" class="d-block"></div>
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded">
                        <h5>Ưu Đãi Đặc Biệt</h5>
                        <p>Giảm giá 20% cho đơn hàng đầu tiên</p>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#farmCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#farmCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
            </button>
        </div>

        <!-- Features -->
        <div class="row mb-4">
            ${createFeatureCard("fa-leaf", "text-success", "Hữu Cơ 100%", "Sản phẩm được trồng trọt tự nhiên không sử dụng hóa chất", "border-success")}
            ${createFeatureCard("fa-award", "text-info", "Chứng Nhận", "Đạt chứng nhận GlobalGAP, VietGAP và hữu cơ USDA", "border-info")}
            ${createFeatureCard("fa-truck", "text-warning", "Giao Hàng Nhanh", "Giao hàng tận nơi trong vòng 24h tại Hà Nội", "border-warning")}
        </div>

        <!-- Products -->
        <div class="card mb-4 shadow">
            <div class="card-header bg-success text-white">
                <h4><i class="fa fa-star"></i> Sản Phẩm Nổi Bật</h4>
            </div>
            <div class="card-body">
                <div class="row">
                    ${createProduct("Rau Sạch", "45.000đ/kg", "#28a745")}
                    ${createProduct("Trái Cây", "75.000đ/kg", "#20c997")}
                    ${createProduct("Thịt Sạch", "120.000đ/kg", "#17a2b8")}
                    ${createProduct("Mật Ong", "150.000đ/chai", "#6c757d")}
                </div>
            </div>
        </div>

        <!-- News -->
        <div class="card mb-4 shadow">
            <div class="card-header bg-info text-white">
                <h4><i class="fa fa-newspaper-o"></i> Tin Tức Nông Nghiệp</h4>
            </div>
            <div class="card-body">
                <div class="row">
                    ${createNews("Kỹ Thuật Trồng Rau Mới", "15/10/2023", "Giới thiệu phương pháp trồng rau không cần đất tiết kiệm 70% nước tưới...")}
                    ${createNews("Giống Cây Mới Năng Suất Cao", "10/10/2023", "Giống lúa mới cho năng suất tăng 30% với khả năng chống chịu sâu bệnh tốt...")}
                    ${createNews("Hội Chợ Nông Nghiệp 2023", "05/10/2023", "Tham gia hội chợ nông nghiệp công nghệ cao lớn nhất năm tại Hà Nội...")}
                </div>
            </div>
        </div>
    </div>
    `;
}

function createFeatureCard(icon, iconColor, title, text, borderClass) {
    return `
        <div class="col-md-4 mb-3">
            <div class="card h-100 ${borderClass}">
                <div class="card-body text-center">
                    <i class="fa ${icon} fa-3x ${iconColor} mb-3"></i>
                    <h4 class="card-title">${title}</h4>
                    <p class="card-text">${text}</p>
                </div>
            </div>
        </div>
    `;
}

function createProduct(name, price, color) {
    return `
        <div class="col-md-3 col-sm-6 mb-4">
            <div class="card h-100">
                <div style="width:100%; height:200px; background-color:${color};"></div>
                <div class="card-body">
                    <h5 class="card-title">${name}</h5>
                    <p class="card-text text-success">${price}</p>
                    <div class="d-flex justify-content-between">
                        <button class="btn btn-sm btn-outline-success"><i class="fa fa-eye"></i> Xem</button>
                        <button class="btn btn-sm btn-success"><i class="fa fa-cart-plus"></i> Mua</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function createNews(title, date, content) {
    return `
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div style="width:100%; height:300px; background-color:#6c757d;"></div>
                <div class="card-body">
                    <h5 class="card-title">${title}</h5>
                    <p class="card-text text-muted"><small>Đăng ngày: ${date}</small></p>
                    <p class="card-text">${content}</p>
                    <a href="#" class="btn btn-sm btn-outline-info">Đọc tiếp</a>
                </div>
            </div>
        </div>
    `;
}
