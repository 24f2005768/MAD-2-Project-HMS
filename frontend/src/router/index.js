import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import AdminDashboard from '@/pages/AdminDashboard.vue'
import ViewPatient from '@/pages/AdminDash/ViewPatient.vue'
import ViewDoctor from '@/pages/AdminDash/ViewDoctor.vue'

import PatientDashboard from '@/pages/PatientDashboard.vue'
import DoctorDashboard from '@/pages/DoctorDashboard.vue'
import TestPage from '@/pages/TestPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', component: HomePage},
    {path: '/login', component: LoginPage},
    {path: '/register', component: RegisterPage},
    
    {path: '/admin', component: AdminDashboard},
    {path: '/admin/patient/:pid', component: ViewPatient},
    {path: '/admin/doctor/:did', component: ViewDoctor},

    {path: '/patient', component: PatientDashboard},
    {path: '/doctor', component: DoctorDashboard},
    {path: '/test', component: TestPage}
  ],
})

export default router
