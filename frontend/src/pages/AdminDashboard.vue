<template>
    <div class="container d-flex flex-column align-items-center flex-grow-1">
        <div class = 'row mb-30'>
            <div class="card row" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Patients</h5>
                    <p class="card-text">{{ patients.length }}</p>
                </div>
            </div>

            <div class="card row" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Appointments</h5>
                    <p class="card-text">Numbers</p>
                </div>
            </div>

            <div class="card row" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Doctors</h5>
                    <p class="card-text">Numbers</p>
                </div>
            </div>

            <div class="card row" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">Departments</h5>
                    <p class="card-text">Numbers</p>
                </div>
            </div>
        </div>

        <h2>Patients</h2>
        <table class = 'table table-striped table-hover'>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>DOB</th>
                    <th>Contact Number</th>
                    <th>Email</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="patient in patients">
                    <td>{{ patient.patient_id }}</td>
                    <td>{{ patient.name }}</td>
                    <td>{{ patient.dob }}</td>
                    <td>{{ patient.patient_user.contact_number }}</td>
                    <td>{{ patient.patient_user.email }}</td>
                </tr>
            </tbody>
        </table>

        <h2>Departments</h2>
        <table class = 'table table-striped table-hover'>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="dept in departments">
                    <td>{{ dept.department_id }}</td>
                    <td>{{ dept.name }}</td>
                </tr>
            </tbody>
        </table>

        <h2>Doctors</h2>
        <table class = 'table table-striped table-hover'>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Contact Number</th>
                    <th>Email</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="doctor in doctors">
                    <td>{{ doctor.doctor_id }}</td>
                    <td>{{ doctor.name }}</td>
                    <td>{{ doctor.doctor_user.contact_number }}</td>
                    <td>{{ doctor.doctor_user.email }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashboard',
        data() {
            return {
                patients: [],
                doctors: [],
                departments: []
            }
        },

        methods: {
            async PopulateData() {
                const all_patients = await requestAPI('GET', null, '/patients')
                const all_doctors = await requestAPI('GET', null, '/doctors')
                const all_departments = await requestAPI('GET', null, '/depts')
                
                this.patients = all_patients
                this.doctors = all_doctors
                this.departments = all_departments
            }
        },

        mounted() {
            this.PopulateData()
        }
    }
</script>