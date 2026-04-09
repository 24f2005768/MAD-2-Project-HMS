<template>
    <div class="container d-flex align-items-center justify-content-center flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div v-if="appointment" class = "container">
            <div class = "col">
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active border-bottom" id="v-tab-upcoming-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-upcoming-appointment" type="button" role="tab">
                        Upcoming Appointments ({{ appointment.upcoming_appointment.length }})
                    </button>

                    <button class="nav-link border-bottom" id="v-tab-past-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-past-appointment" type="button" role="tab">
                        Past Appointments ({{ appointment.past_appointment.length }})
                    </button>
                </div>  
            </div>      
            
            <div class="d-flex justify-content-end my-2">
                <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>
                    Go Back
                </button>
            </div>

            <div class = "col">
                <div class = "container">
                    <div class = "d-flex justify-content-between">
                        <h2>Appointment Details</h2>
                    </div>
                </div>

                <!-- Always visible  -->
                <div class = "container">
                    <div class = "row">
                        <!-- photo container  -->
                        <div class = 'col-sm-3 d-flex justify-content-center align-items-center'>
                            <div class = "d-flex flex-column justify-content-center align-items-center">
                                <div>
                                    <img :src="`/images/${doctorPfp}.png`" height="200px">
                                </div>
                                <p><strong>Doctor Name: </strong>Dr. {{ appointment.app_doctor.name }}</p>
                            </div>
                        </div>

                        <!-- information container -->
                        <div class = 'col-9 p-3'>
                            <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ appointment.appointment_id }}</p>
                            <p><strong>Date: </strong>{{ appointment.date }}</p>
                            <p><strong>Time: </strong>{{ appointment.start_time }} - {{ appointment.end_time }}</p>

                            <div v-if="appointment.status == 'Completed'">
                                <p><strong>Diagnosis: </strong>{{ appointment.app_t.diagnosis }}</p>
                                <p><strong>Notes: </strong>{{ appointment.app_t.notes }}</p>
                                <p><strong>Prescription: </strong>{{ appointment.app_t.prescription }}</p>
                                <p><strong>Tests: </strong>{{ appointment.app_t.tests }}</p>
                            </div>

                            <div v-else-if="appointment.status == 'Booked'">
                                <p>The doctor has not provided any diagnosis, notes, prescription or tests yet.</p>
                            </div>

                            <div v-else>
                                <p>This appointment was cancelled or rescheduled.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1 mt-3" id="v-tab-tabContent">
                    
                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade show active w-100" id="v-tab-upcoming-appointment" role="tabpanel">
                        <h4 class = "mb-3">Upcoming Appointments</h4>
                        <div v-if = "appointment.upcoming_appointment.length == 0">
                            <p>No upcoming appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in appointment.upcoming_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                            <div v-if="a.status == 'Booked'">
                                                <div class = "d-flex gap-2 mt-2">
                                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">
                                                        Cancel
                                                    </button>
                                                    
                                                    <button class="btn btn-outline-primary" data-bs-toggle="modal" :data-bs-target="`#rescheduleAppointment-${a.appointment_id}`">
                                                        Reschedule
                                                    </button>

                                                    <!-- modal  -->
                                                    <RescheduleAppointmentModal 
                                                    :doctor_id = "a.app_doctor.doctor_id"
                                                    :appointment_id = "a.appointment_id"
                                                    @error="errorHandler"
                                                    @success="successHandler"/>
                                                </div>
                                            </div>

                                            <div v-else-if="a.status == 'Completed'">
                                                <RouterLink :to='`/patient/appointment/${a.appointment_id}`'>
                                                    <button class = "btn btn-outline-secondary">View Details</button>
                                                </RouterLink>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-past-appointment" role="tabpanel">
                        <h4 class = "mb-3">Past Appointments</h4>
                        <div v-if = "appointment.past_appointment.length == 0">
                            <p>No past appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in appointment.past_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5> 
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <RouterLink :to='`/patient/appointment/${a.appointment_id}`'>
                                                <button class = "btn btn-outline-secondary">View Details</button>
                                            </RouterLink>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>  
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    
    import errorToast from '@/components/errorToast.vue';
    import successToast from '@/components/successToast.vue';

    import RescheduleAppointmentModal from '@/components/PatientDashComp/RescheduleAppointmentModal.vue';

    export default {
        name: "PatientDashViewAppointment",
        data() {
            return {
                appointment: null,
                errorMessage: "",
                successMessage: "",
                patientPfp: null
            }
        },
        components: {
            errorToast,
            successToast,
            RescheduleAppointmentModal
        },
        methods: {
            async get_appointment() {
                try {
                    const apptID = this.$route.params.aid;
                    const display_appointment = await requestAPI("GET", null, `/appointment/${apptID}?all_appointments=true`)
                    this.appointment = display_appointment
                    this.doctorPfp = display_appointment.app_doctor.pfp
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },
            errorHandler(message) {
                this.errorMessage = message
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.successHandler("Appointment cancelled successfully!")
                    this.get_appointment()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            errorHandler(message) {
                this.errorMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.errorMessage = '';
                }, 5000);
            },
            successHandler(message) {
                this.get_appointment()
                this.successMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.successMessage = '';
                }, 5000);
            },
        },
        mounted() {
            this.get_appointment()
        },
        watch: {
            $route(newVal, oldVal) {
                this.get_appointment()
            }
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>