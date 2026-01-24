import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import SignUpPage from '@/pages/SignUpPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import AdminDashboard from '@/pages/AdminDashboard.vue'
import PatientDashboard from '@/pages/PatientDashboard.vue'
import DoctorDashboard from '@/pages/DoctorDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: HomePage},
    {path: '/login', component: LoginPage},
    {path: '/signup', component: SignUpPage},
    {path: '/register', component: RegisterPage},
    {path: '/admin', component: AdminDashboard},
    {path: '/patient', component: PatientDashboard},
    {path: '/doctor', component: DoctorDashboard}
  ],
})

export default router
