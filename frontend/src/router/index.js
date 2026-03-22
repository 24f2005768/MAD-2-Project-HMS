import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'

import AdminDashboard from '@/pages/AdminDashboard.vue'
import ViewPatient from '@/pages/AdminDash/ViewPatient.vue'
import ViewDoctor from '@/pages/AdminDash/ViewDoctor.vue'
import ViewDepartment from '@/pages/AdminDash/ViewDepartment.vue'
import search from '@/pages/AdminDash/search.vue'

import DoctorDashboard from '@/pages/DoctorDashboard.vue'
import DoctorDashViewPatient from '@/pages/DoctorDash/DoctorDashViewPatient.vue'
import DoctorDashViewAppointment from '@/pages/DoctorDash/DoctorDashViewAppointment.vue'
import DoctorSearch from '@/pages/DoctorDash/DoctorSearch.vue'

import PatientDashboard from '@/pages/PatientDashboard.vue'
import PatientDashViewDoctor from '@/pages/PatientDash/PatientDashViewDoctor.vue'
import PatientDashViewDepartment from '@/pages/PatientDash/PatientDashViewDepartment.vue'
import PatientDashViewAppointment from '@/pages/PatientDash/PatientDashViewAppointment.vue'
import PatientSearch from '@/pages/PatientDash/PatientSearch.vue'

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
    {path: '/admin/dept/:deptId', component: ViewDepartment},
    {path: '/admin/search/:query', component: search},

    {path: '/doctor', component: DoctorDashboard},
    {path: '/doctor/patient/:pid', component: DoctorDashViewPatient},
    {path: '/doctor/appointment/:aid', component: DoctorDashViewAppointment},
    {path: '/doctor/search/:query', component: DoctorSearch, name: "doctorSearch"},

    {path: '/patient', component: PatientDashboard},
    {path: '/patient/doctor/:did', component: PatientDashViewDoctor},
    {path: '/patient/dept/:deptId', component: PatientDashViewDepartment},
    {path: '/patient/appointment/:aid', component: PatientDashViewAppointment},
    {path: '/patient/search/:query', component: PatientSearch, name: "patientSearch"},

    {path: '/test', component: TestPage}
  ],
})

export default router
