import {
  fetchMemberships,
  fetchMembershipDetail,
  createOrUpdateMembership,
  deleteMembership
} from './membershipAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';
import { fetchFreeUsers, fetchCurrentUser } from '/static/core/js/api/userAPI.js';
import { routeTo } from '/static/js/router.js';

function renderUI() {
  $('#membership-modal').remove();

  $('#root').html(`
    <div class="membership-container" data-farm-id="" data-farm-slug="">
      <button class="btn btn-success mb-3 add-member" data-farm-id="">
        Thêm thành viên mới
      </button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Họ tên</th>
            <th>Vai trò</th>
            <th>Ngày tham gia</th>
            <th>Quyền duyệt</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="membership-modal" tabindex="-1" aria-hidden="true" aria-labelledby="membershipModalLabel">
      <div class="modal-dialog">
        <form id="membership-form" class="modal-content" novalidate>
          <div class="modal-header">
            <h5 class="modal-title" id="membershipModalLabel">Thông tin thành viên</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Đóng"></button>
          </div>
          <div class="modal-body">
            <input type="hidden" name="farm" value="" />
            <div id="user-field-wrapper" class="mb-3"></div>
            <div class="mb-3">
              <label for="role" class="form-label">Vai trò</label>
              <select id="role" name="role" class="form-select" required>
                <option value="">-- Chọn vai trò --</option>
                <option value="manager">Quản lý</option>
                <option value="assistant_manager">Phó quản lý</option>
                <option value="farmer">Nông dân</option>
                <option value="sales">Nhân viên bán hàng</option>
                <option value="field_supervisor">Giám sát đồng ruộng</option>
              </select>
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" id="can_approve" name="can_approve" class="form-check-input" />
              <label for="can_approve" class="form-check-label">Có quyền duyệt</label>
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" id="is_active" name="is_active" class="form-check-input" checked />
              <label for="is_active" class="form-check-label">Hoạt động</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="submit" id="submit-membership-btn" class="btn btn-primary">Lưu</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
          </div>
        </form>
      </div>
    </div>
  `);
}

function isValidFarmId(farmId) {
  return (typeof farmId === 'number' && !isNaN(farmId)) || (/^\d+$/.test(farmId));
}

function renderMembershipRow(member, farmId, farmSlug, currentUserRole, currentUsername) {
  const firstName = (member.user.first_name || '').trim();
  const lastName = (member.user.last_name || '').trim();
  const fullName = firstName || lastName ? `${firstName} ${lastName}`.trim() : member.user.username;
  console.log(member);

  return `
    <tr data-id="${member.id}">
      <td>${member.user.profile_picture ? `<img src="${member.user.profile_picture}" class="rounded-circle" alt="profile_picture" style="width:50px; height:50px; ;" />` : ''} ${fullName}</td>
      <td>${member.role_display}</td>
      <td>${member.joined_date}</td>
      <td>
        <span class="badge ${member.can_approve ? 'bg-success' : 'bg-secondary'}">
          ${member.can_approve ? 'Có' : 'Không'}
        </span>
      </td>
      <td>
        <span class="badge ${member.is_active ? 'bg-success' : 'bg-secondary'}">
          ${member.is_active ? 'Hoạt động' : 'Ngừng hoạt động'}
        </span>
      </td>
      <td>
        <button class="btn btn-info btn-sm view-member" data-username="${member.user.username}" data-farm-slug="${farmSlug}">
          <i class="fas fa-eye"></i> Xem
        </button>
        <button class="btn btn-sm btn-primary edit-member" data-id="${member.id}" data-farm-id="${farmId}">
          <i class="fas fa-edit"></i> Sửa
        </button>
        <button class="btn btn-sm btn-danger remove-member" data-id="${member.id}" data-farm-id="${farmId}">
          <i class="fas fa-trash"></i> Xoá
        </button>
      </td>
    </tr>
  `;
}

async function loadMembershipList(farmId, currentUsername, currentUserRole, fetchedMemberships, $container, $tbody) {
  console.log('[loadMembershipList] Bắt đầu tải lại thành viên cho farmId:', farmId);
  if (!isValidFarmId(farmId)) {
    showAlert('error', 'Lỗi: farmId truyền vào không hợp lệ. Vui lòng kiểm tra lại!');
    return;
  }

  farmId = Number(farmId);

  $tbody.html('<tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>');

  try {
    const memberships = await fetchMemberships(farmId);
    fetchedMemberships.length = 0;
    fetchedMemberships.push(...memberships);

    if (memberships.length === 0) {
      $tbody.html('<tr><td colspan="6" class="text-center">Chưa có thành viên nào</td></tr>');
      return;
    }

    $tbody.html('');
    for (const member of memberships) {
      $tbody.append(renderMembershipRow(member, farmId, $container.data('farm-slug') || '', currentUserRole, currentUsername));
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    $container.data('current-user-role', currentUserRole);
  } catch (err) {
    showAlert('error', 'Lỗi khi tải danh sách thành viên');
    console.error(err);
  }
}

async function showMembershipForm(farmId, membershipId, membershipModal) {
  if (!isValidFarmId(farmId)) {
    showAlert('error', 'Lỗi: farmId không hợp lệ khi mở form.');
    return;
  }
  farmId = Number(farmId);

  const $form = $('#membership-form')[0];
  $form.reset();
  $form.dataset.membershipId = membershipId || '';
  const farmInput = $form.querySelector('[name="farm"]');
  if (farmInput) {
    farmInput.dataset.id = farmId;
    farmInput.value = farmId;
  }

  const $userFieldWrapper = $('#user-field-wrapper');

  try {
    if (membershipId) {
      const data = await fetchMembershipDetail(membershipId);
      $userFieldWrapper.html(`
        <input type="text" class="form-control" name="username" value="${data.user.username}" readonly />
      `);
      $('#role').val(data.role);
      $('#can_approve').prop('checked', data.can_approve);
      $('#is_active').prop('checked', data.is_active);
      membershipModal.show();
    } else {
      const users = await fetchFreeUsers(farmId);
      if (users.length === 0) {
        $userFieldWrapper.html(`<p class="text-danger">Không còn người dùng nào có thể thêm.</p>`);
      } else {
        const fixedUsers = users.map(u => Object.fromEntries(u));
        const options = fixedUsers.map(u => {
          const name = u.first_name || u.last_name ? `${u.first_name || ''} ${u.last_name || ''}`.trim() : u.username;
          return `<option value="${u.id}">${name}</option>`;
        }).join('');
        $userFieldWrapper.html(`
          <select class="form-select" name="user_id" required>
            <option value="">-- Chọn người dùng --</option>
            ${options}
          </select>
        `);
      }
      $('#role').val('farmer');
      $('#can_approve').prop('checked', false);
      $('#is_active').prop('checked', true);
      membershipModal.show();
    }
  } catch (error) {
    console.error('Lỗi khi tải dữ liệu:', error);
    showAlert('error', error.message || 'Lỗi khi tải dữ liệu.');
  }
}

function bindEvents(membershipModal, fetchedMemberships, lastFetchedUser) {
  // Unbind trước khi bind để tránh bind nhiều lần
  $(document).off('submit', '#membership-form');
  $(document).off('click', '.remove-member');
  $(document).off('click', '.view-member');
  $(document).off('click', '.add-member');
  $(document).off('click', '.edit-member');

  $(document).on('submit', '#membership-form', async function (e) {
    e.preventDefault();
    const $form = $(this)[0];

    const farmIdRaw = $form.querySelector('[name="farm"]').dataset.id;
    if (!isValidFarmId(farmIdRaw)) {
      showAlert('error', 'Lỗi: farmId không hợp lệ khi gửi form.');
      return;
    }
    const farmId = Number(farmIdRaw);

    const membershipId = $form.dataset.membershipId || null;
    const role = $form['role']?.value;
    if (!role) {
      showAlert('warning', 'Vui lòng chọn vai trò.');
      return;
    }

    const data = {
      farm_id: farmId,
      role: role,
      can_approve: $form['can_approve']?.checked || false,
      is_active: $form['is_active']?.checked ?? true,
    };
    if (!membershipId) {
      const userId = $form['user_id']?.value;
      if (!userId) {
        showAlert('warning', 'Vui lòng chọn người dùng.');
        return;
      }
      data.user_id = parseInt(userId, 10);
    }
    try {
      // Gọi API tạo hoặc cập nhật
      const updatedMember = await createOrUpdateMembership(farmId, membershipId, data);
      membershipModal.hide();

      const $container = $('.membership-container');
      const $tbody = $container.find('tbody');

      if (membershipId) {
        // Sửa thành viên
        // Cập nhật fetchedMemberships
        const index = fetchedMemberships.findIndex(m => m.id === updatedMember.id);
        if (index !== -1) {
          fetchedMemberships[index] = updatedMember;
        } else {
          fetchedMemberships.push(updatedMember);
        }

        // Cập nhật row trong bảng
        const $row = $tbody.find(`tr[data-id="${updatedMember.id}"]`);
        if ($row.length) {
          $row.replaceWith(renderMembershipRow(updatedMember, farmId, $container.data('farm-slug') || '', lastFetchedUser.role, lastFetchedUser.username));
        } else {
          // Nếu chưa có row (trường hợp hiếm) thì append
          $tbody.append(renderMembershipRow(updatedMember, farmId, $container.data('farm-slug') || '', lastFetchedUser.role, lastFetchedUser.username));
        }

        showAlert('success', 'Cập nhật thành viên thành công');
      } else {
        // Thêm thành viên mới
        fetchedMemberships.push(updatedMember);
        $tbody.append(renderMembershipRow(updatedMember, farmId, $container.data('farm-slug') || '', lastFetchedUser.role, lastFetchedUser.username));
        showAlert('success', 'Thêm thành viên thành công');
      }

    } catch (xhr) {
      if (xhr.json) {
        try {
          const errors = await xhr.json();
          displayFormErrors('#membership-form', errors);
        } catch {
          showAlert('error', 'Lỗi không xác định khi gửi dữ liệu.');
        }
      } else {
        showAlert('error', 'Lỗi khi gửi dữ liệu.');
      }
      console.error(xhr);
    }
  });


  $(document).on('click', '.remove-member', async function () {
    if (!confirm('Bạn có chắc chắn muốn xóa thành viên này?')) return;

    const farmIdRaw = $(this).data('farm-id');
    if (!isValidFarmId(farmIdRaw)) {
      showAlert('error', 'Lỗi: farmId không hợp lệ khi xóa thành viên.');
      return;
    }
    const membershipId = $(this).data('id');

    try {
      await deleteMembership(membershipId);

      // Cập nhật UI local mà không load lại toàn bộ
      $(`tr[data-id="${membershipId}"]`).remove();

      // Đồng thời cập nhật mảng fetchedMemberships
      const index = fetchedMemberships.findIndex(m => m.id === membershipId);
      if (index !== -1) fetchedMemberships.splice(index, 1);

      showAlert('success', 'Xóa thành viên thành công');
    } catch (error) {
      showAlert('error', 'Lỗi khi xóa thành viên');
      console.error(error);
    }
  });

  $(document).on('click', '.view-member', function () {
    const farmSlug = $(this).data('farm-slug');
    const username = $(this).data('username');
    if (!farmSlug || typeof farmSlug !== 'string') {
      showAlert('error', 'Lỗi: farmSlug không hợp lệ khi xem thành viên.');
      return;
    }
    if (!['admin', 'manager', 'assistant_manager'].includes(lastFetchedUser.role) && username !== lastFetchedUser.username) {
      showAlert('error', 'Bạn chỉ có quyền xem thông tin của chính mình.');
      return;
    }
    const member = fetchedMemberships.find(m => m.user.username === username);

    if (!member) {
      showAlert('error', 'Không tìm thấy dữ liệu thành viên để hiển thị.');
      return;
    }
    sessionStorage.setItem('selectedMember', JSON.stringify(member));
    setTimeout(() => {
      routeTo(`/farm/${farmSlug}/memberships/${username}/detail/`, document.getElementById('root'));
    }, 100);
  });

  $(document).on('click', '.add-member', function () {
    const farmIdRaw = $(this).data('farm-id');
    if (!isValidFarmId(farmIdRaw)) {
      showAlert('error', 'Lỗi: farmId không hợp lệ khi thêm thành viên.');
      return;
    }
    showMembershipForm(Number(farmIdRaw), null, membershipModal);
  });

  $(document).on('click', '.edit-member', function () {
    const farmIdRaw = $(this).data('farm-id');
    const membershipId = $(this).data('id');
    if (!isValidFarmId(farmIdRaw)) {
      showAlert('error', 'Lỗi: farmId không hợp lệ khi sửa thành viên.');
      return;
    }
    showMembershipForm(Number(farmIdRaw), membershipId, membershipModal);
  });
}

export default async function showMembershipPage(farmIdFromLocal, farmSlugFromLocal) {
  if (!isValidFarmId(farmIdFromLocal) || !farmSlugFromLocal) {
    showAlert('error', 'farmId hoặc farmSlug không hợp lệ');
    return;
  }

  renderUI();

  const fetchedMemberships = [];
  const lastFetchedUser = await fetchCurrentUser();

  const $container = $('.membership-container');
  $container.data('farm-id', farmIdFromLocal);
  $container.data('farm-slug', farmSlugFromLocal);
  $container.find('.add-member').data('farm-id', farmIdFromLocal);

  const $tbody = $container.find('tbody');

  await loadMembershipList(farmIdFromLocal, lastFetchedUser.username, lastFetchedUser.role, fetchedMemberships, $container, $tbody);

  const membershipModalEl = document.getElementById('membership-modal');
  const membershipModal = new bootstrap.Modal(membershipModalEl);

  bindEvents(membershipModal, fetchedMemberships, lastFetchedUser);
}

export async function initMemberships() {
  const farmId = parseInt(localStorage.getItem('currentFarmId'), 10);
  const farmSlug = localStorage.getItem('farmSlug');

  if (!farmId || !farmSlug) {
    console.error('[initMemberships] Thiếu farmId hoặc farmSlug trong localStorage');
    showAlert('error', 'Không tìm thấy thông tin nông trại để hiển thị thành viên.');
    return;
  }

  showMembershipPage(farmId, farmSlug);
}

