// common_static/js/modules.js
export const modules = [
  () => import('/static/core/js/module.js'),
  () => import('/static/farm/js/module.js'),
  // thêm app mới chỉ cần thêm dòng này
];
