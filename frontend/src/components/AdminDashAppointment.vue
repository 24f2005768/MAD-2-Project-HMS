<template>
    <h2>Appointments</h2>
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
                appointments: []
            }
        }, 
        methods: {
            async PopulateAppointments() {
                const all_appointments = await requestAPI('GET', null, '/appointments')
                this.appointments = all_appointments
            }
        },
        mounted() {
            this.PopulateAppointments()
        }
    }
</script>