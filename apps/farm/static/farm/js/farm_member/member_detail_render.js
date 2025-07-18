export function renderMemberDetail(data) {
  const {
    role_display,
    joined_date,
    is_active,
    can_approve,
    user = {},
    farms: rawFarms,
    farm: currentFarmData
  } = data;

  // Lấy danh sách nông trại: Ưu tiên rawFarms, fallback về user.farms
  const farmList = Array.isArray(rawFarms)
    ? rawFarms
    : (Array.isArray(user.farms) ? user.farms : []);

  // Ưu tiên user.current_farm, sau đó đến farm trong root
  const currentFarm = user.current_farm || currentFarmData || null;

  return `
    <div class="container my-4" style="max-width: 900px;">
      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">Thông tin thành viên</h5>
      <div class="row mb-4">
        <div class="col-md-6 mb-3"><p><strong>Vai trò trong nông trại:</strong> ${role_display || user.role_display || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày tham gia:</strong> ${joined_date || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Trạng thái hoạt động:</strong> ${is_active ? "Hoạt động" : "Không hoạt động"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Quyền duyệt:</strong> ${can_approve ? "Có" : "Không"}</p></div>
      </div>

      <hr>

      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">Thông tin người dùng</h5>
      <div class="row mb-4">
        <div class="col-md-6 mb-3"><p><strong>Tên đăng nhập:</strong> ${user.username || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Email:</strong> ${user.email || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Họ tên:</strong> ${(user.first_name || '') + ' ' + (user.last_name || '')}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Số điện thoại:</strong> ${user.phone_number || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Địa chỉ:</strong> ${user.address || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Vai trò:</strong> ${user.role_display || user.role || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Đã xác thực:</strong> ${user.is_verified ? "Có" : "Chưa"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày sinh:</strong> ${user.date_of_birth || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày tham gia hệ thống:</strong> ${user.date_joined || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Lần đăng nhập cuối:</strong> ${user.last_login || 'Chưa cập nhật'}</p></div>

        ${user.profile_picture ? `
        <div class="col-12 mb-3">
          <p><strong>Ảnh đại diện:</strong></p>
          <img src="${user.profile_picture}" alt="Ảnh đại diện" class="img-thumbnail" style="max-width: 150px; max-height: 150px; object-fit: cover;">
        </div>` : ''
        }
      </div>

      <hr>

      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">
        Danh sách nông trại thành viên tham gia (${farmList.length})
      </h5>
      <ul class="list-unstyled">
        ${farmList.length ? farmList.map(farm => `
          <li class="bg-light p-3 rounded shadow-sm mb-3">
            <strong>${farm.name}</strong> (${farm.farm_type_display || 'Chưa cập nhật'})<br>
            Diện tích: ${farm.area ?? 'Chưa cập nhật'} ha &nbsp;&nbsp;|&nbsp;&nbsp;
            Vị trí: ${farm.location || "Chưa cập nhật"}<br>
            Ngày thành lập: ${farm.established_date || 'Chưa cập nhật'}<br>
            Trạng thái: ${farm.is_active
              ? '<span class="badge bg-success">Hoạt động</span>'
              : '<span class="badge bg-secondary">Không hoạt động</span>'}<br>
            Số thành viên: ${farm.members_count ?? 0} 
            (<span class="text-success">${farm.active_members_count ?? 0} đang hoạt động</span>)
          </li>
        `).join('') : '<li>Chưa tham gia nông trại nào.</li>'}
      </ul>

      <hr>

      <h5 class="border-bottom border-primary pb-2 mb-3 text-primary">Nông trại hiện tại:</h5>
      <p>${
        currentFarm
          ? `${currentFarm.name} - ${currentFarm.location || 'Chưa cập nhật'}`
          : 'Chưa chọn nông trại hiện tại.'
      }</p>
    </div>
  `;
}
