import {
  fetchFarmDocuments,
  fetchFarmDocumentDetail,
  createOrUpdateFarmDocument,
  deleteFarmDocument,
} from './farmDocumentAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';

let documentModal;

function renderDocumentUI(root) {
  $('#document-modal').remove();

  root.innerHTML = `
    <div class="document-container" data-farm-id="">
      <button class="btn btn-success mb-3 add-document">Thêm tài liệu mới</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Tiêu đề</th>
            <th>Loại tài liệu</th>
            <th>Ngày phát hành</th>
            <th>Ngày hết hạn</th>
            <th>File</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody id="document-list">
          <tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="document-modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <form id="document-form" class="modal-content" novalidate enctype="multipart/form-data">
          <div class="modal-header">
            <h5 class="modal-title">Thông tin tài liệu</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="hidden" id="farm_id" name="farm_id" value="" />
            <div class="mb-3">
              <label for="title" class="form-label">Tiêu đề <span class="text-danger">*</span></label>
              <input type="text" id="title" name="title" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="document_type" class="form-label">Loại tài liệu</label>
              <select id="document_type" name="document_type" class="form-select">
                <option value="contract">Hợp đồng</option>
                <option value="certificate">Chứng nhận</option>
                <option value="license">Giấy phép</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="issue_date" class="form-label">Ngày phát hành</label>
              <input type="date" id="issue_date" name="issue_date" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="expiry_date" class="form-label">Ngày hết hạn</label>
              <input type="date" id="expiry_date" name="expiry_date" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="description" class="form-label">Mô tả</label>
              <textarea id="description" name="description" class="form-control"></textarea>
            </div>
            <div class="mb-3">
              <label for="file" class="form-label">Tệp tin</label>
              <input type="file" id="file" name="file" class="form-control" />
              <div id="current-file-link" class="mt-1"></div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="submit" id="submit-btn" class="btn btn-primary">Lưu</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
          </div>
        </form>
      </div>
    </div>
  `;

  documentModal = new bootstrap.Modal(document.getElementById('document-modal'));
}

function isValidFarmId(farmId) {
  return typeof farmId === 'string' && /^\d+$/.test(farmId);
}

function renderDocumentRow(doc) {
  return `
    <tr data-id="${doc.id}">
      <td>${doc.title}</td>
      <td>${doc.document_type_display || doc.document_type}</td>
      <td>${doc.issue_date || ''}</td>
      <td>${doc.expiry_date || ''}</td>
      <td>
        ${doc.file_url ? `<a href="${doc.file_url}" class="btn btn-outline-primary btn-sm" target="_blank">Xem</a>` : 'Chưa có'}
      </td>
      <td>
        <button class="btn btn-sm btn-primary btn-edit" data-id="${doc.id}"><i class="fas fa-edit"></i> Sửa</button>
        <button class="btn btn-sm btn-danger btn-delete" data-id="${doc.id}"><i class="fas fa-trash"></i> Xoá</button>
      </td>
    </tr>
  `;
}

async function loadDocumentList(farmId) {
  const $tbody = $('#document-list');
  let timeout = setTimeout(() => {
    $tbody.html('<tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>');
  }, 150);

  const start = performance.now();

  try {
    const docs = await fetchFarmDocuments(farmId);
    clearTimeout(timeout);
    const elapsed = performance.now() - start;
    const delay = Math.max(0, 400 - elapsed);

    setTimeout(() => {
      if (!docs || docs.length === 0) {
        $tbody.html('<tr><td colspan="6" class="text-center">Chưa có tài liệu</td></tr>');
        return;
      }
      $tbody.html(docs.map(renderDocumentRow).join(''));
    }, delay);
  } catch (error) {
    clearTimeout(timeout);
    showAlert('danger', 'Lỗi khi tải danh sách tài liệu');
  }
}

function resetForm() {
  const $form = $('#document-form')[0];
  $form.reset();
  $('#document-form').removeAttr('data-id');
  $('#submit-btn').text('Tạo tài liệu');
  $('#current-file-link').empty();
  $('.form-control').removeClass('is-invalid');
}

async function showDocumentForm(farmId, documentId = null) {
  resetForm();
  $('#farm_id').val(farmId);
  $('#document-form').attr('data-farm-id', farmId);
  $('#document-form').attr('data-id', documentId || '');

  if (documentId) {
    $('#submit-btn').text('Đang tải...');
    try {
      const doc = await fetchFarmDocumentDetail(documentId);
      $('#title').val(doc.title);
      $('#document_type').val(doc.document_type);
      $('#issue_date').val(doc.issue_date);
      $('#expiry_date').val(doc.expiry_date);
      $('#description').val(doc.description);

      if (doc.file_url) {
        $('#current-file-link').html(`<a href="${doc.file_url}" target="_blank">File hiện tại</a>`);
      }

      $('#submit-btn').text('Cập nhật tài liệu');
      documentModal.show();
    } catch (error) {
      showAlert('danger', 'Không thể tải thông tin tài liệu');
    }
  } else {
    documentModal.show();
  }
}

function bindDocumentEvents() {
  // Gỡ sự kiện cũ để tránh trùng lặp
  $(document).off('submit', '#document-form');
  $(document).off('click', '.add-document');
  $(document).off('click', '.btn-edit');
  $(document).off('click', '.btn-delete');

  $(document).on('submit', '#document-form', async function (e) {
    e.preventDefault();

    const $form = $(this);
    const farmId = $form.attr('data-farm-id');
    const docId = $form.attr('data-id') || null;
    const formData = new FormData(this);

    if (!docId && !formData.has('farm_id')) {
      formData.append('farm_id', farmId);
    }

    const fileInput = document.getElementById('file');
    if (docId && !fileInput.files.length) {
      formData.delete('file');
    }

    const $submitBtn = $('#submit-btn');
    $submitBtn.prop('disabled', true).text(docId ? 'Đang cập nhật...' : 'Đang tạo...');

    $('.form-control').removeClass('is-invalid');
    $('.invalid-feedback').remove();

    try {
      const newDoc = await createOrUpdateFarmDocument(farmId, docId, formData);

      documentModal.hide();

      // Cập nhật DOM mà không load lại toàn bộ
      const $row = $(`#document-list tr[data-id="${newDoc.id}"]`);
      if (docId && $row.length) {
        // Đang sửa -> replace dòng
        $row.replaceWith(renderDocumentRow(newDoc));
      } else {
        // Đang tạo mới -> thêm dòng mới
        $('#document-list').append(renderDocumentRow(newDoc));
      }

      showAlert('success', docId ? 'Cập nhật thành công' : 'Tạo tài liệu thành công');
    } catch (error) {
      const errors = error?.responseJSON || null;
      if (errors) {
        displayFormErrors('#document-form', errors);
      } else {
        showAlert('danger', 'Lỗi khi lưu tài liệu');
      }
    } finally {
      $submitBtn.prop('disabled', false).text(docId ? 'Cập nhật tài liệu' : 'Tạo tài liệu');
    }
  });

  $(document).on('click', '.add-document', () => {
    const farmId = $('.document-container').data('farm-id');
    showDocumentForm(farmId);
  });

  $(document).on('click', '.btn-edit', function () {
    const farmId = $('.document-container').data('farm-id');
    const docId = $(this).data('id');
    showDocumentForm(farmId, docId);
  });

  $(document).on('click', '.btn-delete', async function () {
    const farmId = $('.document-container').data('farm-id');
    const docId = $(this).data('id');

    if (confirm('Bạn có chắc muốn xoá tài liệu này không?')) {
      try {
        await deleteFarmDocument(docId);
        $(`#document-list tr[data-id="${docId}"]`).remove();
        showAlert('success', 'Xoá thành công');
      } catch {
        showAlert('danger', 'Lỗi khi xoá tài liệu');
      }
    }
  });
}

export async function initDocuments() {
  renderDocumentUI(root);
  bindDocumentEvents();

  const farmIdFromLocal = localStorage.getItem('currentFarmId');
  if (isValidFarmId(farmIdFromLocal)) {
    $('.document-container').attr('data-farm-id', farmIdFromLocal);
    await loadDocumentList(farmIdFromLocal);
  }
}
