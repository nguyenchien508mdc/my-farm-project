import { renderAdminSidebar } from './sidebar/adminSidebar.js';
import { renderCustomerSidebar } from './sidebar/customerSidebar.js';
import { renderStaffSidebar } from './sidebar/staffSidebar.js';


export function renderSidebar(user) {
    const role = user?.role || '';

    if (role === 'admin') {
        return renderAdminSidebar();
    } else if (role === 'customer') {
        return renderCustomerSidebar();
    }else if (role === 'staff') {
        return renderStaffSidebar();
    } else {
        return `
        <div class="sidebar-sticky pt-2">
            <p>Chưa đăng nhập hoặc không có quyền truy cập.</p>
        </div>
        `;
    }
}
