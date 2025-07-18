import {
  fetchFarmDocuments,
  fetchFarmDocumentDetail,
  createOrUpdateFarmDocument,
  deleteFarmDocument,
} from './farmDocumentAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';

export function initDocuments() {
    $(function () {
    // 1. Render UI vào div#root
    function renderUI() {
        $('#root').html(`
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

        <!-- Modal tài liệu -->
        <div class="modal fade" id="document-modal" tabindex="-1" aria-hidden="true" aria-labelledby="documentModalLabel">
            <div class="modal-dialog">
            <input type="hidden" id="farm_id" name="farm_id" value="" />
            <form id="document-form" class="modal-content" novalidate enctype="multipart/form-data">
                <div class="modal-header">
                <h5 class="modal-title" id="documentModalLabel">Thông tin tài liệu</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Đóng"></button>
                </div>
                <div class="modal-body">
                <div class="mb-3">
                    <label for="title" class="form-label">Tiêu đề <span class="text-danger">*</span></label>
                    <input type="text" id="title" name="title" class="form-control" required />
                </div>
                <div class="mb-3">
                    <label for="document_type" class="form-label">Loại tài liệu</label>
                    <select id="document_type" name="document_type" class="form-select">
                    <option value="contract">Hợp đồng</option>
                    <option value="certificate">Giấy chứng nhận</option>
                    <option value="other">Khác</option>
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
                    <textarea id="description" name="description" class="form-control" rows="3"></textarea>
                </div>
                <div class="mb-3">
                    <label for="file" class="form-label">Tệp tin</label>
                    <input type="file" id="file" name="file" class="form-control" />
                    <div id="current-file-link" class="mt-1"></div>
                </div>
                </div>
                <div class="modal-footer">
                <button type="submit" id="submit-btn" class="btn btn-primary">Tạo tài liệu</button>
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                </div>
            </form>
            </div>
        </div>
        `);
    }

    renderUI();

    const documentModal = new bootstrap.Modal(document.getElementById('document-modal'));

    // 2. Hàm render 1 dòng tài liệu
    function renderDocumentRow(doc) {
        return `
        <tr data-id="${doc.id}">
            <td>${doc.title}</td>
            <td>${doc.document_type_display || doc.document_type}</td>
            <td>${doc.issue_date || ''}</td>
            <td>${doc.expiry_date || ''}</td>
            <td>
            ${
                doc.file_url
                ? `<a href="${doc.file_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-eye"></i> Xem
                    </a>`
                : 'Chưa có'
            }
            </td>
            <td>
            <button class="btn btn-sm btn-primary btn-edit" data-id="${doc.id}">
                <i class="fas fa-edit"></i> Sửa
            </button>
            <button class="btn btn-sm btn-danger btn-delete" data-id="${doc.id}">
                <i class="fas fa-trash"></i> Xoá
            </button>
            </td>
        </tr>
        `;
    }

    // 3. Load danh sách tài liệu theo farmId
    function loadDocumentList(farmId) {
        const $tbody = $('#document-list');
        $tbody.html('<tr><td colspan="6" class="text-center text-muted">Đang tải...</td></tr>');

        fetchFarmDocuments(farmId, function (documents) {
        if (!documents || documents.length === 0) {
            $tbody.html('<tr><td colspan="6" class="text-center text-muted">Chưa có tài liệu nào</td></tr>');
            return;
        }

        const rows = documents.map(renderDocumentRow).join('');
        $tbody.html(rows);
        }, function () {
        showAlert('danger', 'Lỗi khi tải danh sách tài liệu');
        });
    }

    // 4. Reset form modal
    function resetForm() {
        const form = $('#document-form')[0];
        form.reset();
        $('#document-form').removeAttr('data-id');
        $('#document-form .form-control').removeClass('is-invalid');
        $('.invalid-feedback').empty();
        $('#submit-btn').html('Tạo tài liệu');
        $('#current-file-link').empty();
    }

    // 5. Hiển thị form tạo/sửa tài liệu
    function showDocumentForm(farmId, documentId = null) {
        resetForm();
        $('#document-form').attr('data-farm-id', farmId);
        $('#document-form').attr('data-id', documentId || '');
        $('#farm_id').val(farmId);

        if (documentId) {
        $('#submit-btn').html('Đang tải...');
        fetchFarmDocumentDetail(documentId, function (doc) {
            $('#title').val(doc.title);
            $('#document_type').val(doc.document_type);
            $('#issue_date').val(doc.issue_date);
            $('#expiry_date').val(doc.expiry_date);
            $('#description').val(doc.description);

            if (doc.file_url) {
            $('#current-file-link').html(`<a href="${doc.file_url}" target="_blank">File hiện tại</a>`);
            } else {
            $('#current-file-link').empty();
            }

            $('#submit-btn').html('Cập nhật tài liệu');
            documentModal.show();
        }, function () {
            showAlert('danger', 'Lỗi khi tải thông tin tài liệu');
        });
        } else {
        $('#submit-btn').html('Tạo tài liệu');
        $('#current-file-link').empty();
        documentModal.show();
        }
    }

    // 6. Submit form tạo hoặc cập nhật tài liệu
    $(document).on('submit', '#document-form', function (e) {
        e.preventDefault();

        const farmId = $(this).attr('data-farm-id');
        const documentId = $(this).attr('data-id') || null;
        const formData = new FormData(this);

        createOrUpdateFarmDocument(farmId, documentId, formData, function () {
        documentModal.hide();
        loadDocumentList(farmId);
        showAlert('success', documentId ? 'Cập nhật tài liệu thành công' : 'Tạo tài liệu thành công');
        }, function (xhr) {
        const errors = xhr.responseJSON || null;
        if (errors && typeof displayFormErrors === 'function') {
            displayFormErrors('#document-form', errors);
        } else {
            showAlert('danger', 'Lỗi khi lưu tài liệu');
        }
        });
    });

    // 7. Sự kiện thêm tài liệu mới
    $(document).on('click', '.add-document', function () {
        const farmId = $('.document-container').data('farm-id');
        showDocumentForm(farmId, null);
    });

    // 8. Sự kiện sửa tài liệu
    $(document).on('click', '.btn-edit', function () {
        const farmId = $('.document-container').data('farm-id');
        const docId = $(this).data('id');
        showDocumentForm(farmId, docId);
    });

    // 9. Sự kiện xóa tài liệu
    $(document).on('click', '.btn-delete', function () {
        const farmId = $('.document-container').data('farm-id');
        const docId = $(this).data('id');

        if (confirm('Bạn có chắc chắn muốn xoá tài liệu này?')) {
        deleteFarmDocument(docId, function () {
            loadDocumentList(farmId);
            showAlert('success', 'Xoá tài liệu thành công');
        }, function () {
            showAlert('danger', 'Lỗi khi xoá tài liệu');
        });
        }
    });

    // 10. Khởi tạo: Lấy farmId từ localStorage load danh sách
    const farmId = localStorage.getItem('currentFarmId');

    if (farmId) {
        $('.document-container').attr('data-farm-id', farmId);
        loadDocumentList(farmId);
    } else {
        $('#document-list').html('<tr><td colspan="6" class="text-center text-muted">Không có farmId để tải tài liệu</td></tr>');
    }
    });
};