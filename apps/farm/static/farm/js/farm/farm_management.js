import { fetchFarmList, createOrUpdateFarm, deleteFarm, fetchFarmDetail } from './farmAPI.js';
import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';
import { routeTo } from '/static/js/router.js';

let farmFormModal;

function renderFarmUI(root) {
    $('#farm-form-modal').remove(); 
    root.innerHTML = `
        <button class="btn btn-success mb-3 create-farm">Tạo mới nông trại</button>
        <div id="farm-list-container">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Tên</th><th>Vị trí</th><th>Diện tích (ha)</th><th>Loại</th><th>Thành viên</th><th>Trạng thái</th><th>Hành động</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <!-- Modal Bootstrap -->
        <div class="modal fade" id="farm-form-modal" tabindex="-1" aria-hidden="true" aria-labelledby="farmFormModalLabel">
            <div class="modal-dialog">
                <form id="farm-form" class="modal-content" novalidate>
                    <div class="modal-header">
                        <h5 class="modal-title" id="farmFormModalLabel">Thông tin nông trại</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Đóng"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="farm-name" class="form-label">Tên <span class="text-danger">*</span></label>
                            <input type="text" class="form-control" id="farm-name" name="name" required />
                        </div>
                        <div class="mb-3">
                            <label for="farm-location" class="form-label">Vị trí</label>
                            <input type="text" class="form-control" id="farm-location" name="location" />
                        </div>
                        <div class="mb-3">
                            <label for="farm-area" class="form-label">Diện tích (ha)</label>
                            <input type="number" step="0.01" class="form-control" id="farm-area" name="area" />
                        </div>
                        <div class="mb-3">
                            <label for="farm-type" class="form-label">Loại</label>
                            <select class="form-select" id="farm-type" name="farm_type">
                                <option value="plant">Trồng trọt</option>
                                <option value="livestock">Chăn nuôi</option>
                                <option value="mixed">Kết hợp</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="farm-description" class="form-label">Mô tả</label>
                            <textarea class="form-control" id="farm-description" name="description" rows="3"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="farm-established-date" class="form-label">Ngày thành lập</label>
                            <input type="date" class="form-control" id="farm-established-date" name="established_date" />
                        </div>
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="farm-is-active" name="is_active" checked />
                            <label class="form-check-label" for="farm-is-active">Hoạt động</label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Lưu</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    farmFormModal = new bootstrap.Modal(document.getElementById('farm-form-modal'));
}

function loadFarmList() {
    fetchFarmList(function (data) {
        let html = '';
        if (!data || data.length === 0) {
            html = `<tr><td colspan="7" class="text-center">Không có nông trại nào</td></tr>`;
        } else {
            data.forEach(farm => {
                html += `
                    <tr>
                        <td>${farm.name}</td>
                        <td>${farm.location || ''}</td>
                        <td>${farm.area || ''}</td>
                        <td>${farm.farm_type_display || farm.farm_type || 'plant'}</td>
                        <td>${farm.members_count || 0}</td>
                        <td>
                            <span class="badge bg-${farm.is_active ? 'success' : 'secondary'}">
                                ${farm.is_active ? 'Hoạt động' : 'Ngừng hoạt động'}
                            </span>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-primary edit-farm" data-id="${farm.id}"><i class="fas fa-edit"></i> Sửa</button>
                            <button class="btn btn-sm btn-danger delete-farm" data-id="${farm.id}"><i class="fas fa-trash"></i> Xoá</button>
                            <button class="btn btn-sm btn-info show-membership" data-farm-slug="${farm.slug}" data-farm-id="${farm.id}"><i class="fas fa-user"></i> Xem</button>
                            <button class="btn btn-sm btn-warning show-documents" data-farm-slug="${farm.slug}" data-farm-id="${farm.id}"><i class="fas fa-file"></i> Xem</button>
                        </td>
                    </tr>
                `;
            });
        }
        $('#farm-list-container table tbody').html(html);
    }, function () {
        showAlert('error', 'Lỗi khi tải danh sách nông trại');
    });
}

function showFarmForm(id = null) {
    const $form = $('#farm-form');
    if (id) {
        fetchFarmDetail(id, function (data) {
            $form.find('input[name="name"]').val(data.name || '');
            $form.find('input[name="location"]').val(data.location || '');
            $form.find('input[name="area"]').val(data.area || '');
            $form.find('select[name="farm_type"]').val(data.farm_type || 'plant');
            $form.find('textarea[name="description"]').val(data.description || '');
            $form.find('input[name="established_date"]').val(data.established_date || '');
            $form.find('input[name="is_active"]').prop('checked', data.is_active === true);

            $form.data('id', id);

            $form.find('.is-invalid').removeClass('is-invalid');
            $form.find('.invalid-feedback').remove();

            farmFormModal.show();
        }, function () {
            alert('Lỗi khi tải dữ liệu nông trại');
        });
    } else {
        $form[0].reset();
        $form.removeData('id');
        $form.find('.is-invalid').removeClass('is-invalid');
        $form.find('.invalid-feedback').remove();
        $form.find('input[name="is_active"]').prop('checked', true);
        $form.find('select[name="farm_type"]').val('plant');

        farmFormModal.show();
    }
}

function bindFarmEvents() {
    // Gỡ bỏ sự kiện cũ tránh trùng lặp
    $(document).off('submit', '#farm-form');
    $(document).off('click', '.create-farm');
    $(document).off('click', '.edit-farm');
    $(document).off('click', '.delete-farm');
    $(document).off('click', '.show-membership');
    $(document).off('click', '.show-documents');

    $(document).on('submit', '#farm-form', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const id = $(this).data('id');
        const isActiveChecked = $(this).find('input[name="is_active"]').is(':checked');
        formData.set('is_active', isActiveChecked);
        const farmType = $(this).find('select[name="farm_type"]').val();
        formData.set('farm_type', farmType);

        createOrUpdateFarm(id, formData, function () {
            farmFormModal.hide();
            loadFarmList();
            showAlert('success', id ? 'Cập nhật thành công' : 'Tạo mới thành công');
        }, function (xhr) {
            const errors = xhr.responseJSON || { '__all__': ['Lỗi không xác định'] };
            displayFormErrors('#farm-form', errors);
        });
    });

    $(document).on('click', '.create-farm', () => showFarmForm());
    $(document).on('click', '.edit-farm', function () {
        showFarmForm($(this).data('id'));
    });
    $(document).on('click', '.delete-farm', function () {
        if (!confirm('Bạn có chắc chắn muốn xóa nông trại này?')) return;
        deleteFarm($(this).data('id'), () => {
            loadFarmList();
            showAlert('success', 'Xóa thành công');
        }, () => {
            showAlert('error', 'Lỗi khi xóa nông trại');
        });
    });
    $(document).on('click', '.show-membership', function () {
        const farmSlug = $(this).data('farm-slug');
        const farmId = $(this).data('farm-id');
        if (farmId) localStorage.setItem('currentFarmId', farmId);
        if (farmSlug) localStorage.setItem('farmSlug', farmSlug);
        routeTo(`/farm/${farmSlug}/members/`, document.getElementById('root'));
    });
    $(document).on('click', '.show-documents', function () {
        const farmSlug = $(this).data('farm-slug');
        const farmId = $(this).data('farm-id');
        if (farmId) localStorage.setItem('currentFarmId', farmId);
        if (farmSlug) localStorage.setItem('farmSlug', farmSlug);
        routeTo(`/farm/${farmSlug}/documents/`, document.getElementById('root'));
    });
}

export async function initFarm() {
    renderFarmUI(root);
    bindFarmEvents();
    loadFarmList();
}
