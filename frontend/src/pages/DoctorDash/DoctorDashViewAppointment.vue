<template>
    <div class="container d-flex align-items-center justify-content-center flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

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
                                    <img :src="`/images/${patientPfp}.png`" height="200px" width="200px">
                                </div>
                                <p><strong>Patient Name: </strong>{{ appointment.app_patient.name }}</p>
                            </div>
                        </div>

                        <!-- information container -->
                        <div class = 'col-9 p-3'>
                            <div class = "d-flex justify-content-between">
                                <p><strong>Date: </strong>{{ appointment.date }}</p>
                                <button v-if="appointment.status == 'Completed'" class = "btn btn-outline-primary" data-bs-toggle = "modal" data-bs-target = "#update-treatment-modal">
                                    Update Details
                                </button>

                                <!-- modal  -->
                                <UpdateTreatmentModal 
                                :appointment = "appointment"
                                @update-treatment = "updateTreatmentDetails"/>
                            </div>
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
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
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
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                            <div v-if="a.status == 'Booked'">
                                                <div class = "d-flex gap-2 mt-2">
                                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                                    <button class = "btn btn-outline-primary">Reschedule</button>
                                                </div>
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
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <button class = "btn btn-outline-secondary">View Details</button>
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
    import errorToast from '@/components/errorToast.vue';
    import { requestAPI } from '../../../utils/api';

    import UpdateTreatmentModal from '@/components/DoctorDashComp/UpdateTreatmentModal.vue';

    export default {
        name: "DoctorDashViewAppointment",
        data() {
            return {
                appointment: null,
                errorMessage: null,
                patientPfp: null
            }
        },
        components: {
            errorToast,
            UpdateTreatmentModal
        },
        methods: {
            async get_appointment() {
                try {
                    const apptID = this.$route.params.aid;
                    const display_appointment = await requestAPI("GET", null, `/appointment/${apptID}?all_appointments=true`)
                    this.appointment = display_appointment
                    this.patientPfp = display_appointment.app_patient.pfp
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },
            errorHandler(message) {
                this.errorMessage = message
            },
            async updateTreatmentDetails(data) {
                try {
                    console.log(data)
                    const apptID = this.$route.params.aid;
                    const update_appointment = await requestAPI("PATCH", data, `/treatment/${apptID}`)
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            }
        },
        mounted() {
            this.get_appointment()
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>