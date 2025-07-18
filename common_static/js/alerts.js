// common_static\js\alerts.js
export function showAlert(type, message) {
    const alertClassMap = {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
    };

    const alertClass = alertClassMap[type] || 'alert-secondary'; // fallback nếu type không hợp lệ

    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;

    $('#alert-container').html(alertHtml);
    setTimeout(() => $('.alert').alert('close'), 3000);
}
