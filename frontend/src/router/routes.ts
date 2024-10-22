import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/admin',
    component: () => import('layouts/AdminLayout.vue'),
    children: [
      { path: '', component: () => import('pages/admin/AdminDashboard.vue') },
    ],
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LandingPage.vue') },
      {
        path: '/login',
        component: () => import('pages/LoginPage.vue'),
      },
      {
        path: '/dashboard',
        component: () => import('pages/DashboardPage.vue'),
        meta: { requiresAuth: true, role: 'user' }

      },
      {
        path: '/registration',
        component: () => import('pages/RegistrationPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    name: "not-found",
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
