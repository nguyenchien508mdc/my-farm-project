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
                            <label for="farm-logo" class="form-label">Logo</label>
                            <input type="file" class="form-control" id="farm-logo" name="logo" accept="image/*" />
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

function renderFarmRow(farm) {
  return `
    <tr>
      <td>${farm.logo ? `<img src="${farm.logo}" class="rounded-circle"  alt="Logo" style="width:50px; height:50px;;" />` : ''} ${farm.name}</td>
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
}

async function loadFarmList() {
  const $tbody = $('#farm-list-container table tbody');
  $tbody.html('<tr><td colspan="7" class="text-center text-muted">Đang tải...</td></tr>');

  try {
    const data = await fetchFarmList();
    if (!data || data.length === 0) {
      $tbody.html('<tr><td colspan="7" class="text-center">Không có nông trại nào</td></tr>');
      return;
    }

    $tbody.html(''); 

    let index = 0;
    function appendNextFarm() {
      if (index >= data.length) return;
      const farm = data[index];
      $tbody.append(renderFarmRow(farm));
      index++;
      setTimeout(appendNextFarm, 100); 
    }
    appendNextFarm();

  } catch (error) {
    showAlert('error', 'Lỗi khi tải danh sách nông trại');
  }
}

function showLogoPreview(fileInput) {
  const file = fileInput.files[0];
  if (!file) {
    $('#farm-logo-preview').remove();
    return;
  }
  if ($('#farm-logo-preview').length === 0) {
    $('<img id="farm-logo-preview" style="max-width:100px; margin-bottom:10px;" />').insertBefore(fileInput);
  }
  const reader = new FileReader();
  reader.onload = function(e) {
    $('#farm-logo-preview').attr('src', e.target.result);
  };
  reader.readAsDataURL(file);
}

async function showFarmForm(id = null) {
  const $form = $('#farm-form');
  if (id) {
    try {
      const data = await fetchFarmDetail(id);

      $form.find('input[name="name"]').val(data.name || '');
      $form.find('input[name="location"]').val(data.location || '');
      $form.find('input[name="area"]').val(data.area || '');
      $form.find('select[name="farm_type"]').val(data.farm_type || 'plant');
      $form.find('textarea[name="description"]').val(data.description || '');
      $form.find('input[name="established_date"]').val(data.established_date || '');
      $form.find('input[name="is_active"]').prop('checked', !!data.is_active);

      // Hiển thị logo preview nếu có URL logo
      if (data.logo) {
        if ($('#farm-logo-preview').length === 0) {
          $('<img id="farm-logo-preview" style="max-width:100px; margin-bottom:10px;" />').insertBefore('#farm-logo');
        }
        $('#farm-logo-preview').attr('src', data.logo);
      } else {
        $('#farm-logo-preview').remove();
      }

      $form.data('id', id);
      $form.find('.is-invalid').removeClass('is-invalid');
      $form.find('.invalid-feedback').remove();

      farmFormModal.show();
    } catch {
      alert('Lỗi khi tải dữ liệu nông trại');
    }
  } else {
    $form[0].reset();
    $form.removeData('id');
    $('#farm-logo-preview').remove();
    $form.find('.is-invalid').removeClass('is-invalid');
    $form.find('.invalid-feedback').remove();
    $form.find('input[name="is_active"]').prop('checked', true);
    $form.find('select[name="farm_type"]').val('plant');
    farmFormModal.show();
  }
}

// Thêm event lắng nghe file input để hiện preview logo khi chọn file mới
$(document).on('change', '#farm-logo', function () {
  showLogoPreview(this);
});

function bindFarmEvents() {
    $(document).off('submit', '#farm-form');
    $(document).off('click', '.create-farm');
    $(document).off('click', '.edit-farm');
    $(document).off('click', '.delete-farm');
    $(document).off('click', '.show-membership');
    $(document).off('click', '.show-documents');

    $(document).on('submit', '#farm-form', async function (e) {
      e.preventDefault();

      const formElement = this;
      const formData = new FormData(formElement);
      const id = $(formElement).data('id');

      // is_active checkbox
      const isActiveInput = formElement.querySelector('input[name="is_active"]');
      formData.set('is_active', isActiveInput.checked ? 'true' : 'false');

      // area
      const area = formData.get('area');
      if (area && area.trim() !== '') {
        formData.set('area', parseFloat(area));
      } else {
        formData.set('area', '');
      }

      // established_date
      const establishedDate = formData.get('established_date');
      if (!establishedDate || establishedDate.trim() === '') {
        formData.set('established_date', '');
      }

      // Nếu không chọn logo mới => xóa trường logo
      const logoInput = formElement.querySelector('input[name="logo"]');
      if (logoInput && logoInput.files.length === 0) {
        formData.delete('logo');
      }

      try {
        const newFarm = await createOrUpdateFarm(id, formData);
        farmFormModal.hide();

        const $tbody = $('#farm-list-container table tbody');
        const $rows = $tbody.find('tr');
        let found = false;

        // Nếu đang sửa → cập nhật lại row
        if (id) {
          $rows.each(function () {
            const $row = $(this);
            const $editBtn = $row.find('.edit-farm');
            if ($editBtn.data('id') === newFarm.id) {
              $row.replaceWith(renderFarmRow(newFarm));
              found = true;
            }
          });
        }

        // Nếu không tìm thấy row (tức là tạo mới) → append cuối
        if (!found) {
          $tbody.append(renderFarmRow(newFarm));
        }

        showAlert('success', id ? 'Cập nhật thành công' : 'Tạo mới thành công');
      } catch (xhr) {
        const errors = xhr.responseJSON || { '__all__': ['Lỗi không xác định'] };
        displayFormErrors('#farm-form', errors);
      }
    });

    $(document).on('click', '.create-farm', () => showFarmForm());

    $(document).on('click', '.edit-farm', function () {
        showFarmForm($(this).data('id'));
    });

    $(document).on('click', '.delete-farm', async function () {
      if (!confirm('Bạn có chắc chắn muốn xóa nông trại này?')) return;

      const farmId = $(this).data('id');
      try {
        await deleteFarm(farmId);
        $(`#farm-list-container table tbody tr`).each(function () {
          const $row = $(this);
          if ($row.find('.edit-farm').data('id') === farmId) {
            $row.remove();
          }
        });
        showAlert('success', 'Xóa thành công');
      } catch {
        showAlert('error', 'Lỗi khi xóa nông trại');
      }
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
    await loadFarmList();
}
