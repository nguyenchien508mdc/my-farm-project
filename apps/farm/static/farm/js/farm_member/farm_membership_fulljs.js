import {
  fetchMemberships,
  fetchMembershipDetail,
  createOrUpdateMembership,
  deleteMembership
} from './membershipAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';
import { fetchFreeUsers, fetchCurrentUser } from '/static/core/js/api/userAPI.js';

export function initMemberships() {
    $(function () {
    // 1. Render giao diện chính trong #root
    function renderUI() {
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

        <!-- Modal thành viên -->
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
                    <option value="assistant_manager">Trợ lý quản lý</option>
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

    renderUI();

    // Bootstrap 5 modal instance
    const membershipModal = new bootstrap.Modal(document.getElementById('membership-modal'));

    // 2. Validate farmId
    function isValidFarmId(farmId) {
        return (typeof farmId === 'number' && !isNaN(farmId)) || (/^\d+$/.test(farmId));
    }

    // 3. Render row thành viên
    function renderMembershipRow(member, farmId, farmSlug, currentUserRole, currentUsername) {
        const firstName = (member.user.first_name || '').trim();
        const lastName = (member.user.last_name || '').trim();
        const fullName = firstName || lastName
        ? `${firstName} ${lastName}`.trim()
        : member.user.username;

        return `
        <tr data-id="${member.id}">
            <td>${fullName}</td>
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

    let fetchedMemberships = [];

    // 4. Load danh sách thành viên
    function loadMembershipList(farmId, currentUsername, currentUserRole) {
        if (!isValidFarmId(farmId)) {
        console.error('[Error] loadMembershipList: farmId không hợp lệ:', farmId);
        showAlert('error', 'Lỗi: farmId truyền vào không hợp lệ. Vui lòng kiểm tra lại!');
        return;
        }
        farmId = Number(farmId);

        const $container = $(`.membership-container[data-farm-id="${farmId}"]`);
        const farmSlug = $container.data('farm-slug') || '';
        const $tbody = $container.find('tbody');
        $tbody.html('<tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>');

        fetchMemberships(farmId, (memberships) => {
        fetchedMemberships = memberships;
        console.log(fetchedMemberships)
        if (memberships.length === 0) {
            $tbody.html('<tr><td colspan="6" class="text-center">Chưa có thành viên nào</td></tr>');
            return;
        }

        const rows = memberships.map(m => renderMembershipRow(m, farmId, farmSlug, currentUserRole, currentUsername)).join('');
        $tbody.html(rows);

        // Lưu role hiện tại vào data attribute để các thao tác dùng nếu cần
        $container.data('current-user-role', currentUserRole);
        }, () => {
        showAlert('error', 'Lỗi khi tải danh sách thành viên');
        });
    }

    // 5. Hiển thị form thêm/sửa thành viên
    function showMembershipForm(farmId, membershipId = null) {
        if (!isValidFarmId(farmId)) {
        console.error('[Error] showMembershipForm: farmId không hợp lệ:', farmId);
        showAlert('error', 'Lỗi: farmId truyền vào không hợp lệ khi mở form.');
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

        if (membershipId) {
        fetchMembershipDetail(membershipId, (data) => {
            $userFieldWrapper.html(`
            <input type="text" class="form-control" name="username" value="${data.user.username}" readonly />
            `);
            $('#role').val(data.role);
            $('#can_approve').prop('checked', data.can_approve);
            $('#is_active').prop('checked', data.is_active);
            membershipModal.show();
        }, () => {
            showAlert('error', 'Lỗi khi tải thông tin thành viên');
        });
        } else {
        fetchFreeUsers(farmId, (users) => {
            if (users.length === 0) {
            $userFieldWrapper.html(`<p class="text-danger">Không còn người dùng nào có thể thêm.</p>`);
            } else {
            const options = users.map(u =>
                `<option value="${u.id}">${u.first_name || u.last_name ? `${u.first_name} ${u.last_name}`.trim() : u.username}</option>`
            ).join('');
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
        }, () => {
            $userFieldWrapper.html(`<p class="text-danger">Lỗi khi tải danh sách người dùng.</p>`);
        });
        }
    }

    // 6. Submit form thêm/sửa thành viên
    $(document).on('submit', '#membership-form', function (e) {
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
        farm: Number(farmId),
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
        data.user = userId;
        }

        createOrUpdateMembership(farmId, membershipId, data, () => {
        membershipModal.hide();
        loadMembershipList(farmId, lastFetchedUser.username, lastFetchedUser.role);
        showAlert('success', membershipId ? 'Cập nhật thành viên thành công' : 'Thêm thành viên thành công');
        }, (xhr) => {
        const errors = xhr.responseJSON || null;
        displayFormErrors('#membership-form', errors);
        });
    });

    // 7. Xóa thành viên
    $(document).on('click', '.remove-member', function () {
        if (!confirm('Bạn có chắc chắn muốn xóa thành viên này?')) return;

        const farmIdRaw = $(this).data('farm-id');
        if (!isValidFarmId(farmIdRaw)) {
        showAlert('error', 'Lỗi: farmId không hợp lệ khi xóa thành viên.');
        return;
        }
        const farmId = Number(farmIdRaw);
        const membershipId = $(this).data('id');

        deleteMembership(membershipId, () => {
        loadMembershipList(farmId, lastFetchedUser.username, lastFetchedUser.role);
        showAlert('success', 'Xóa thành viên thành công');
        }, () => {
        showAlert('error', 'Lỗi khi xóa thành viên');
        });
    });

    // 8. Xem thành viên
    $(document).on('click', '.view-member', function () {
        const farmSlug = $(this).data('farm-slug');
        const username = $(this).data('username');
        if (!farmSlug || typeof farmSlug !== 'string') {
        showAlert('error', 'Lỗi: farmSlug không hợp lệ khi xem thành viên.');
        return;
        }
        if (!['admin', 'manager', 'assistant_manager'].includes(lastFetchedUser.role) && username !== lastFetchedUser.username) {
        alert('Bạn chỉ có quyền xem thông tin của chính mình.');
        return;
        }
        const member = fetchedMemberships.find(m => m.user.username === username);

        if (!member) {
        showAlert('error', 'Không tìm thấy dữ liệu thành viên để hiển thị.');
        return;
        }
        sessionStorage.setItem('selectedMember', JSON.stringify(member));
        setTimeout(() => {
        window.location.href = `/farm/${farmSlug}/memberships/${username}/detail/`;
        }, 100);
    });

    // 9. Thêm thành viên
    $(document).on('click', '.add-member', function () {
        const farmIdRaw = $(this).data('farm-id');

        if (!isValidFarmId(farmIdRaw)) {
        showAlert('error', 'Lỗi: farmId không hợp lệ khi thêm thành viên.');
        return;
        }

        showMembershipForm(Number(farmIdRaw), null);
    });

    // 10. Sửa thành viên
    $(document).on('click', '.edit-member', function () {
        const farmIdRaw = $(this).data('farm-id');
        const membershipId = $(this).data('id');

        if (!isValidFarmId(farmIdRaw)) {
        showAlert('error', 'Lỗi: farmId không hợp lệ khi sửa thành viên.');
        return;
        }

        showMembershipForm(Number(farmIdRaw), membershipId);
    });

    // 11. Lưu user hiện tại để dùng khi gọi load danh sách
    let lastFetchedUser = { username: '', role: '' };

    // 12. Lấy user hiện tại rồi load danh sách
    fetchCurrentUser((user) => {
        lastFetchedUser.username = user.username;
        lastFetchedUser.role = user.role || '';

        const $container = $('.membership-container');
        if ($container.length === 0) {
            console.warn('[Warning] Không tìm thấy container membership-container trên trang');
            return;
        }
        const farmIdFromLocal = localStorage.getItem('currentFarmId');
        const farmSlugFromLocal = localStorage.getItem('farmSlug') || 'example-farm';

        if (!farmIdFromLocal) {
            showAlert('error', 'Không tìm thấy currentFarmId trong localStorage');
            return;
        }

        const farmId = Number(farmIdFromLocal);
        if (isNaN(farmId)) {
            showAlert('error', 'currentFarmId trong localStorage không hợp lệ');
            return;
        }

        $container.attr('data-farm-id', farmId.toString());
        $container.attr('data-farm-slug', farmSlugFromLocal);
        $container.find('.add-member').attr('data-farm-id', farmIdFromLocal);

        const farmIdRaw = $container.data('farm-id');
        if (!farmIdRaw) {
            console.warn('[Warning] membership-container không có data-farm-id!');
            return;
        }

        if (!isValidFarmId(farmIdRaw)) {
            console.error('[Error] membership-container data-farm-id không hợp lệ:', farmIdRaw);
            showAlert('error', 'Lỗi: data-farm-id trên DOM không hợp lệ.');
            return;
        }

        loadMembershipList(Number(farmIdRaw), lastFetchedUser.username, lastFetchedUser.role);
    }, () => {
        showAlert('error', 'Lỗi khi lấy thông tin người dùng hiện tại. Vui lòng đăng nhập lại.');
        window.location.href = '/login/';
    });
    });
};