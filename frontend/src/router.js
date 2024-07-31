import { createRouter, createWebHistory } from 'vue-router';
import AdminUsers from './components/AdminUsers.vue';
import AdminBooks from "./components/AdminBooks.vue";
import UserDashboard from './components/UserDashboard.vue';
import Login from './components/Login.vue';
import Register from "./components/Register.vue";
import AdminDashboard from './components/AdminDashboard.vue';
import AdminSections from "./components/AdminSections.vue";
import AdminRequests from "./components/AdminRequests.vue";
import BookHistory from "./components/BookHIstory.vue";
import UserBooks from "./components/UserBooks.vue";

const routes = [
  { path: '/admin/dashboard', name:'AdminDashboard', component: AdminDashboard },
  { path: '/admin/users', name:'AdminUsers', component: AdminUsers },
  { path: '/admin/books', name: 'AdminBooks', component: AdminBooks},
  { path: '/admin/sections', name: AdminSections, component: AdminSections},
  { path: '/admin/requests', name: AdminRequests, component: AdminRequests},
  { path: '/user/dashboard', name:'UserDashboard',  component: UserDashboard },
  { path: '/login', name:'Login', component: Login, alias: '/' },
  { path: '/admin/books/:bookId/history', name: 'BookHistory', component: BookHistory},
  { path: '/book/issued', name: 'BookIssued', component: UserBooks},
  { path: '/register',name:'Register', component: Register }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
