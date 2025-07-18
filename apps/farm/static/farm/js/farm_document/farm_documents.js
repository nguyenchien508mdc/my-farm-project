// apps\farm\static\js\farm_documents.js
import {
    fetchFarmDocuments,
    fetchFarmDocumentDetail,
    createOrUpdateFarmDocument,
    deleteFarmDocument
} from './farmDocumentAPI.js';

import { displayFormErrors } from '/static/js/formHandler.js';
import { showAlert } from '/static/js/alerts.js';
 
$(function () {
    function renderDocumentRow(doc) {
        return `
            <tr data-id="${doc.id}">
                <td>${doc.title}</td>
                <td>${doc.document_type_display}</td>
                <td>${doc.issue_date}</td>
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

    function showDocumentForm(farmId, documentId = null) {
        resetForm();
        $('#document-form').attr('data-id', documentId || '');
        $('#document-form').attr('data-farm-id', farmId);
        const $modal = $('#document-modal');

        if (documentId) {
            $('#submit-btn').html('Đang tải...');
            fetchFarmDocumentDetail(farmId, documentId, function (doc) {
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
                
                $modal.modal('show');
            }, function () {
                showAlert('danger', 'Lỗi khi tải thông tin tài liệu');
            });
        } else {
            $('#submit-btn').html('Tạo tài liệu');
            $('#current-file-link').empty();
            $modal.modal('show');
        }
    }

    function resetForm() {
        const form = $('#document-form')[0];
        form.reset();
        $('#document-form').removeAttr('data-id');
        $('#document-form .form-control').removeClass('is-invalid');
        $('.invalid-feedback').empty();
        $('#submit-btn').html('Tạo tài liệu');
    }

    $('#document-form').on('submit', function (e) {
        e.preventDefault();

        const farmId = $(this).attr('data-farm-id');
        const documentId = $(this).attr('data-id') || null;
        const formData = new FormData(this);

        createOrUpdateFarmDocument(farmId, documentId, formData, function () {
            $('#document-modal').modal('hide');
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

    $(document).on('click', '.add-document', function () {
        const farmId = $('.document-container').data('farm-id');
        showDocumentForm(farmId, null);
    });

    $(document).on('click', '.btn-edit', function () {
        const farmId = $('.document-container').data('farm-id');
        const docId = $(this).data('id');
        showDocumentForm(farmId, docId);
    });

    $(document).on('click', '.btn-delete', function () {
        const farmId = $('.document-container').data('farm-id');
        const docId = $(this).data('id');

        if (confirm('Bạn có chắc chắn muốn xoá tài liệu này?')) {
            deleteFarmDocument(farmId, docId, function () {
                loadDocumentList(farmId);
                showAlert('success', 'Xoá tài liệu thành công');
            }, function () {
                showAlert('danger', 'Lỗi khi xoá tài liệu');
            });
        }
    });

    $(function () {
        const $container = $('.document-container');
        if ($container.length) {
            const farmId = $container.data('farm-id');
            loadDocumentList(farmId);
        }
    });
});
