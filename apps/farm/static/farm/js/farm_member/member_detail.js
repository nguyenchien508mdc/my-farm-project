// apps\farm\static\farm\js\farm_member\member_detail.js
import { renderMemberDetail } from './member_detail_render.js';
import { routeTo } from '/static/js/router.js';

export async function initFarmMembershipDetail() {
  if (!root) {
    console.error('Không tìm thấy phần tử root để render');
    return;
  }

  const memberJson = sessionStorage.getItem('selectedMember');
  if (!memberJson) {
    root.innerHTML = `<div class="alert alert-warning">Không tìm thấy dữ liệu thành viên. Vui lòng quay lại trang danh sách và thử lại.</div>`;
    return;
  }

  try {
    const memberData = JSON.parse(memberJson);
    root.innerHTML = renderMemberDetail(memberData);
    document.getElementById('backToListBtn')?.addEventListener('click', () => {
      sessionStorage.removeItem('selectedMember');
      routeTo(`/farm/${memberData.farm.slug}/members/`, document.getElementById('root')); 
    });
  } catch (error) {
    console.error('Lỗi khi phân tích dữ liệu thành viên hoặc lấy farms:', error);
    root.innerHTML = `<div class="alert alert-danger">Dữ liệu thành viên không hợp lệ hoặc lỗi lấy dữ liệu nông trại.</div>`;
  }
}