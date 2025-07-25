// static/core/js/module.js

export const coreRoutes = {
  '/': () => import('./home.js').then(m => m.createHomePage),

  '/login/': () => import('./auth/login.js').then(m => m.initLogin),
  '/register/': () => import('./auth/register.js').then(m => m.initRegister),
  '/password-reset/': () => import('./auth/password_reset.js').then(m => m.initPasswordReset),
  '^/password-reset-confirm/.+/.+/$': () => import('./auth/password_reset_confirm.js').then(m => m.initPasswordResetConfirm),

  '/users/': () => import('./users/users.js').then(m => m.initUsers),
  '/password-change/': () => import('./users/password_change.js').then(m => m.initPasswordChange),
  '/profile/': () => import('./users/profile.js').then(m => m.initProfile),
  '/profile-update/': () => import('./users/profile_update.js').then(m => m.initProfileUpdate),
};
