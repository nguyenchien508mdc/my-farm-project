// apps\farm\static\js\farm_management.js
import { fetchFarmList, createOrUpdateFarm, deleteFarm , fetchFarmDetail } from './farmAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';

$(document).ready(function() {
    // Load danh sách farm và hiển thị bảng
    function loadFarmList() {
        fetchFarmList(function(data) {
            let html = '';
            if (!data || data.length === 0) {
                html = `<tr><td colspan="7" class="text-center">Không có nông trại nào</td></tr>`;
            } else {
                data.forEach(farm => {
                    html += `
                        <tr>
                            <td>${farm.name}</td>
                            <td>${farm.location || ''}</td>
                            <td>${farm.area || ''} ha</td>
                            <td>${farm.farm_type_display || farm.farm_type || ''}</td>
                            <td>${farm.members_count || 0}</td>
                            <td>
                                <span class="badge bg-${farm.is_active ? 'success' : 'secondary'}">
                                    ${farm.is_active ? 'Hoạt động' : 'Ngừng hoạt động'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-primary edit-farm" data-id="${farm.id}"><i class="fas fa-edit"></i> Sửa</button>
                                <button class="btn btn-sm btn-danger delete-farm" data-id="${farm.id}"><i class="fas fa-trash"></i> Xoá</button>
                                <button class="btn btn-sm btn-info show-membership" data-farm-slug="${farm.slug}"><i class="fas fa-user"></i> Xem</button>
                                <button class="btn btn-sm btn-warning show-documents" data-farm-slug="${farm.slug}"><i class="fas fa-file"></i> Xem</button>
                            </td>
                        </tr>
                    `;
                });
            }
            $('#farm-list-container table tbody').html(html);
        }, function() {
            showAlert('error', 'Lỗi khi tải danh sách nông trại');
        });
    }

    // Hiển thị form tạo hoặc sửa farm trong modal
    function showFarmForm(id = null) {
    const $form = $('#farm-form');
    if (id) {
        fetchFarmDetail(id, function(data) {
            // Điền dữ liệu vào form
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

            $('#farm-form-modal').modal('show');
        }, function() {
            alert('Lỗi khi tải dữ liệu nông trại');
        });
    } else {
        $form[0].reset();
        $form.removeData('id');

        $form.find('.is-invalid').removeClass('is-invalid');
        $form.find('.invalid-feedback').remove();
        $form.find('input[name="is_active"]').prop('checked', true);
        $form.find('select[name="farm_type"]').val('plant');

        $('#farm-form-modal').modal('show');
    }
}

    // Submit form tạo hoặc cập nhật farm
    $(document).on('submit', '#farm-form', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const id = $(this).data('id');
        const isActiveChecked = $(this).find('input[name="is_active"]').is(':checked');
        formData.set('is_active', isActiveChecked);
        
        createOrUpdateFarm(id, formData, function(response) {
            $('#farm-form-modal').modal('hide');
            loadFarmList();
            showAlert('success', id ? 'Cập nhật thành công' : 'Tạo mới thành công');
        }, function(xhr) {
            const errors = xhr.responseJSON || { '__all__': ['Lỗi không xác định'] };
            displayFormErrors('#farm-form', errors);
        });
    });

    // Sự kiện click tạo farm mới
    $(document).on('click', '.create-farm', function() {
        showFarmForm();
    });

    // Sự kiện click sửa farm
    $(document).on('click', '.edit-farm', function() {
        const id = $(this).data('id');
        showFarmForm(id);
    });

    // Sự kiện xóa farm
    $(document).on('click', '.delete-farm', function() {
        if (!confirm('Bạn có chắc chắn muốn xóa nông trại này?')) return;
        const id = $(this).data('id');
        deleteFarm(id, function() {
            loadFarmList();
            showAlert('success', 'Xóa thành công');
        }, function() {
            showAlert('error', 'Lỗi khi xóa nông trại');
        });
    });

    // Xem danh sách thành viên farm
    $(document).on('click', '.show-membership', function() {
        const farmSlug = $(this).data('farm-slug');
        window.location.href = `/farm/${farmSlug}/members/`;
    });

    // Xem danh sách tài liệu farm
    $(document).on('click', '.show-documents', function() {
        const farmSlug = $(this).data('farm-slug');
        window.location.href = `/farm/${farmSlug}/documents/`;
    });

    // Load farm list lúc đầu
    loadFarmList();
});
