export function renderMemberDetail(memberData) {
  const {
    role_display: memberRoleDisplay,
    joined_date: memberJoinedDate,
    is_active: memberIsActive,
    can_approve: memberCanApprove,
    user: userInfo = {},
    farms: memberFarmListFromRoot,
    farm: fallbackCurrentFarm
  } = memberData;

  // Lấy danh sách nông trại mà thành viên tham gia:
  const participatingFarms = Array.isArray(memberFarmListFromRoot)
    ? memberFarmListFromRoot
    : (Array.isArray(userInfo.farms) ? userInfo.farms : []);

  // Xác định nông trại hiện tại:
  const currentFarm = userInfo.current_farm || fallbackCurrentFarm || null;

  return `
    <div class="container my-4" style="max-width: 900px;">
      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">Thông tin thành viên</h5>
      <div class="row mb-4">
        <div class="col-md-6 mb-3"><p><strong>Vai trò trong nông trại:</strong> ${memberRoleDisplay || userInfo.role_display || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày tham gia:</strong> ${memberJoinedDate || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Trạng thái hoạt động:</strong> ${memberIsActive ? "Hoạt động" : "Không hoạt động"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Quyền duyệt:</strong> ${memberCanApprove ? "Có" : "Không"}</p></div>
      </div>

      <hr>

      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">Thông tin người dùng</h5>
      <div class="row mb-4">
        <div class="col-md-6 mb-3"><p><strong>Tên đăng nhập:</strong> ${userInfo.username || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Email:</strong> ${userInfo.email || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Họ tên:</strong> ${(userInfo.first_name || '') + ' ' + (userInfo.last_name || '')}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Số điện thoại:</strong> ${userInfo.phone_number || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Địa chỉ:</strong> ${userInfo.address || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Vai trò:</strong> ${userInfo.role_display || userInfo.role || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Đã xác thực:</strong> ${userInfo.is_verified ? "Có" : "Chưa"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày sinh:</strong> ${userInfo.date_of_birth || "Chưa cập nhật"}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Ngày tham gia hệ thống:</strong> ${userInfo.date_joined || 'Chưa cập nhật'}</p></div>
        <div class="col-md-6 mb-3"><p><strong>Lần đăng nhập cuối:</strong> ${userInfo.last_login || 'Chưa cập nhật'}</p></div>

        ${userInfo.profile_picture ? `
        <div class="col-12 mb-3">
          <p><strong>Ảnh đại diện:</strong></p>
          <img src="${userInfo.profile_picture}" alt="Ảnh đại diện" class="img-thumbnail" style="max-width: 150px; max-height: 150px; object-fit: cover;">
        </div>` : ''
        }
      </div>

      <hr>

      <h5 class="border-bottom border-primary pb-2 mb-4 text-primary">
        Danh sách nông trại thành viên tham gia (${participatingFarms.length})
      </h5>
      <ul class="list-unstyled">
        ${participatingFarms.length ? participatingFarms.map(farm => `
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
          ? `${currentFarm.name || 'Chưa có tên'} - ${currentFarm.location || 'Chưa cập nhật địa điểm'}`
          : 'Chưa chọn nông trại hiện tại.'
      }</p>
    </div>
    <div class="text-end mt-4">
      <button id="backToListBtn" class="btn btn-outline-primary">
        ← Quay lại danh sách
      </button>
    </div>
  `;
}
