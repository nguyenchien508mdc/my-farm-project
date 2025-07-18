//apps\farm\static\js\farm_membership.js
import {
    fetchMemberships,
    fetchMembershipDetail,
    createOrUpdateMembership,
    deleteMembership
} from './membershipAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';
import { fetchFreeUsers, fetchCurrentUser } from '/static/js/userAPI.js';

$(function () {
    // Kiểm tra farmId hợp lệ
    function isValidFarmId(farmId) {
        return (typeof farmId === 'number' && !isNaN(farmId)) || (/^\d+$/.test(farmId));
    }

    // Hàm tạo row thành viên, thêm tham số role để quyết định hiển thị nút sửa, xoá
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

    // Load danh sách thành viên, cập nhật quyền trong hàm
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

    // Hiển thị form thêm/sửa thành viên
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
            fetchMembershipDetail(farmId, membershipId, (data) => {
                $userFieldWrapper.html(`
                    <input type="text" class="form-control" name="username" value="${data.user.username}" readonly />
                `);
                $('#role').val(data.role);
                $('#can_approve').prop('checked', data.can_approve);
                $('#is_active').prop('checked', data.is_active);
                $('#membership-modal').modal('show');
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
                $('#membership-modal').modal('show');
            }, () => {
                $userFieldWrapper.html(`<p class="text-danger">Lỗi khi tải danh sách người dùng.</p>`);
            });
        }
    }

    // Submit form thêm/sửa
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
            $('#membership-modal').modal('hide');
            loadMembershipList(farmId, lastFetchedUser.username, lastFetchedUser.role);
            showAlert('success', membershipId ? 'Cập nhật thành viên thành công' : 'Thêm thành viên thành công');
        }, (xhr) => {
            const errors = xhr.responseJSON || null;
            displayFormErrors('#membership-form', errors);
        });
    });

    // Xóa thành viên
    $(document).on('click', '.remove-member', function () {
        if (!confirm('Bạn có chắc chắn muốn xóa thành viên này?')) return;

        const farmIdRaw = $(this).data('farm-id');
        if (!isValidFarmId(farmIdRaw)) {
            showAlert('error', 'Lỗi: farmId không hợp lệ khi xóa thành viên.');
            return;
        }
        const farmId = Number(farmIdRaw);
        const membershipId = $(this).data('id');

        deleteMembership(farmId, membershipId, () => {
            loadMembershipList(farmId, lastFetchedUser.username, lastFetchedUser.role);
            showAlert('success', 'Xóa thành viên thành công');
        }, () => {
            showAlert('error', 'Lỗi khi xóa thành viên');
        });
    });

    // Xem thành viên
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
            window.location.href = `/farm/${farmSlug}/farm-memberships/${username}/detail/`;
        }, 100);
    });



    // Thêm thành viên
    $(document).on('click', '.add-member', function () {
        const farmIdRaw = $(this).data('farm-id');

        if (!isValidFarmId(farmIdRaw)) {
            showAlert('error', 'Lỗi: farmId không hợp lệ khi thêm thành viên.');
            return;
        }

        showMembershipForm(Number(farmIdRaw), null);
    });

    // Sửa thành viên
    $(document).on('click', '.edit-member', function () {
        const farmIdRaw = $(this).data('farm-id');
        const membershipId = $(this).data('id');

        if (!isValidFarmId(farmIdRaw)) {
            showAlert('error', 'Lỗi: farmId không hợp lệ khi sửa thành viên.');
            return;
        }

        showMembershipForm(Number(farmIdRaw), membershipId);
    });

    // Biến lưu user hiện tại để dùng ở các chỗ khác
    let lastFetchedUser = { username: '', role: '' };

    // Load danh sách khi trang load: gọi API lấy user hiện tại trước
    fetchCurrentUser((user) => {
        lastFetchedUser.username = user.username;
        lastFetchedUser.role = user.role || '';

        $('.membership-container').each(function () {
            const farmIdRaw = $(this).data('farm-id');

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
        });
    }, () => {
        showAlert('error', 'Lỗi khi lấy thông tin người dùng hiện tại. Vui lòng đăng nhập lại.');
        window.location.href = '/login/';
    });
});
