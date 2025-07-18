// apps\farm\static\farm\js\farm_member\member_detail.js
import { renderMemberDetail } from './member_detail_render.js';
import { authHeaders } from '/static/js/auth.js';

async function fetchMemberFarms(userId) {
  try {
    const res = await fetch(`/api/farm/users/${userId}/all-farms/`, {
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
    });
    if (!res.ok) throw new Error(`Lỗi khi lấy dữ liệu nông trại: ${res.status}`);
    const data = await res.json();
    return data.farms ?? [];
  } catch (error) {
    console.error('Lỗi fetchMemberFarms:', error);
    return [];
  }
}

export async function initFarmMembershipDetail() {
  const root = document.getElementById('root');
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
    console.log(memberData)
    // if (memberData?.user?.id) {
    //   memberData.farms = await fetchMemberFarms(memberData.user.id);
    // } else {
    //   memberData.farms = [];
    // }
    root.innerHTML = renderMemberDetail(memberData);
  } catch (error) {
    console.error('Lỗi khi phân tích dữ liệu thành viên hoặc lấy farms:', error);
    root.innerHTML = `<div class="alert alert-danger">Dữ liệu thành viên không hợp lệ hoặc lỗi lấy dữ liệu nông trại.</div>`;
  }
}