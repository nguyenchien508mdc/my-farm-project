// apps\farm\static\farm\js\module.js

export const farmRoutes = {
    '/farm/': () => import('./farm/farm_management.js').then(m => m.initFarm),
    '^/farm/[^/]+/members/?$': () => import('./farm_member/farm_membership.js').then(m => m.initMemberships),
    '^/farm/[^/]+/documents/?$': () => import('./farm_document/farm_documents.js').then(m => m.initDocuments),
    '^/farm/[^/]+/memberships/[^/]+/detail/?$': () =>import('./farm_member/member_detail.js').then(m => m.initFarmMembershipDetail),
};
