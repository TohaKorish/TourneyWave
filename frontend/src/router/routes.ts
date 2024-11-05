import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/admin',
    component: () => import('layouts/AdminLayout.vue'),
    children: [
      { path: '', component: () => import('pages/admin/AdminDashboard.vue') },
      { path: 'games', component: () => import('pages/admin/games/GamesListingPage.vue') },
      { path: 'games/new', component: () => import('pages/admin/games/GamesFormPage.vue') },
      { path: 'games/edit/:id', component: () => import('pages/admin/games/GamesFormPage.vue') },
    ],
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/frontend/LandingPage.vue') },
      { path: '/login', component: () => import('pages/frontend/LoginPage.vue'), },
      { path: '/dashboard', component: () => import('pages/frontend/DashboardPage.vue'), meta: { requiresAuth: true, role: 'user' } },
      { path: '/registration', component: () => import('pages/frontend/RegistrationPage.vue'), },
      { path: '/matches', component: () => import('pages/frontend/MatchesPage.vue'), meta: { requiresAuth: true, role: 'user' }},
      { path: '/matches/:id', component: () => import('pages/frontend/MatchRoomPage.vue'), meta: { requiresAuth: true, role: 'user' }},
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
