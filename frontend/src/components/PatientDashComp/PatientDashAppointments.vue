<template>
    <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#bookAppointment" v-on:click="PopulatePatientsDoctors()">
        Book Appointment
    </button>

    <!-- modal  -->
     <BookAppointmentModal />
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    import BookAppointmentModal from './BookAppointmentModal.vue';

    export default {
        name: 'PatientDashAppointments',
        emits: ['error'],
        data() {
            return {
                all_doctors: null
            }
        }, 
        components: {
            BookAppointmentModal
        },
        methods: {
            async PopulatePatientsDoctors() {
                const allDoctors = await requestAPI("GET", null, "/doctors")
                this.all_doctors = allDoctors
            }
        }
    }
</script>