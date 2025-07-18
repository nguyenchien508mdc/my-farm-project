// common_static\js\routes.js
import { modules } from './modules.js';

let allRoutes = {};

async function loadRoutes() {
  for (const loadModule of modules) {
    const mod = await loadModule();
    const routes = Object.values(mod).find(v => typeof v === 'object' && v !== null);
    if (routes) {
      Object.assign(allRoutes, routes);
    }
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadRoutes();

  const path = window.location.pathname;
  for (const pattern in allRoutes) {
    const isMatch = pattern.startsWith('^') ? new RegExp(pattern).test(path) : pattern === path;
    if (isMatch) {
      const initFunc = await allRoutes[pattern]();
      if (typeof initFunc === 'function') initFunc();
      break;
    }
  }
});
