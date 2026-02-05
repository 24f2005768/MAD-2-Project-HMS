<template>
    <div class = 'container'>
        <div class = "d-flex justify-content-between">
            <h2>Appointments</h2>

            <button class = 'btn btn-primary' type="button" data-bs-toggle="collapse" data-bs-target="#add-apt-button" v-on:click="PopulatePatientsDoctors">
                Add
            </button>
        </div>
    </div>

    <!-- Add appointment  -->
     <p v-show="patient">{{ patient }}</p>
    <div class = "collapse" id = "add-apt-button">
        <div class = "container">
            <div class = "row">
                <div class = "col">
                    <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            Dropdown Patients
                        </button>

                        <!-- Patients  -->
                        <ul class="dropdown-menu">
                            <li v-for = "patient in all_patients"><a class = "dropdown-item" v-on:click = "`selectPatient(${patient_id})`">{{ patient.name }}</a></li>
                        </ul>
                    </div>
                </div>
                
                <div class = "col">
                    <div class = "dropdown">
                        <button class = "btn btn-secondary dropdown-toggle" type = "button" data-bs-toggle = "dropdown">
                            Dropdown Doctors
                        </button>

                        <!-- Doctors  -->
                        <ul class="dropdown-menu">
                            <li v-for = "doctor in all_doctors"><a class = "dropdown-item">{{ doctor.name }}</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <table class = 'table table-striped table-hover'>
        <thead>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for = 'a in appointments'>
                <td>{{ a.appointment_id }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.app_patient.name }}</td>
                <td>{{ a.app_doctor.name }}</td>
                <td>{{ a.status }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashAppointment',
        data() {
            return {
                appointments: [],
                patient: null,
                doctor: null,
                all_patients: null,
                all_doctors: null
            }
        }, 
        methods: {
            async PopulateAppointments() {
                const all_appointments = await requestAPI('GET', null, '/appointments')
                this.appointments = all_appointments
            },
            
            async PopulatePatientsDoctors() {
                const allPatients = await requestAPI("GET", null, "/patients")
                this.all_patients = allPatients

                const allDoctors = await requestAPI("GET", null, "/doctors")
                this.all_doctors = allDoctors
            },

            async selectPatient(patient_id) {
                const selected_patient = await requestAPI("GET", null, `/patient/${patient_id}`)
                this.patient = selected_patient
            }
        },
        mounted() {
            this.PopulateAppointments()
        }
    }
</script>