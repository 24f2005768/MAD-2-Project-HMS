<template>
    <div class="container d-flex align-items-center justify-content-center flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div v-if="patient" class = "container">
            <div class = "col">
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active border-bottom" id="v-tab-upcoming-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-upcoming-appointment" type="button" role="tab">
                        Upcoming Appointments ({{ patient.upcoming_appointment.length }})
                    </button>

                    <button class="nav-link border-bottom" id="v-tab-past-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-past-appointment" type="button" role="tab">
                        Past Appointments ({{ patient.past_appointment.length }})
                    </button>
                </div>  
            </div>              

            <div class = "col">
                <div class = "container">
                    <div class = "d-flex justify-content-between">
                        <h2>Patient Profile</h2>
                        <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>Go Back</button>
                    </div>
                </div>

                <!-- Always visible  -->
                <div class = "container">
                    <div class = "row">
                        <!-- photo container  -->
                        <div class = 'col-sm-3 d-flex justify-content-center align-items-center'>
                            <div class = "d-flex flex-column justify-content-center align-items-center">
                                <div>
                                    <img :src="`/images/${patient.pfp}.png`" height="200px" width="200px">
                                </div>
                                <p><strong>Name: </strong>{{ patient.name }}</p>
                            </div>
                        </div>

                        <!-- information container -->
                        <div class = 'col-9 p-3'>
                            <p><strong>Gender: </strong>{{ patient.gender }}</p>
                            <p><strong>DOB: </strong>{{ patient.dob }}</p>
                            <p><strong>Age: </strong>{{ patient.get_age }}</p>
                            <p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ patient.patient_user.email }}</p>
                            <p><strong>Height: </strong>{{ patient.height }} cm</p>
                            <p><strong>Weight: </strong>{{ patient.weight }} kg</p>
                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade show active w-100" id="v-tab-upcoming-appointment" role="tabpanel">
                        <h3 class = "mb-3">Upcoming Appointments</h3>
                        <div v-if = "patient.upcoming_appointment.length == 0">
                            <p>No upcoming appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in patient.upcoming_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
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
                                                    :patient_id = "a.app_patient.patient_id"
                                                    :doctor_id = "a.app_doctor.doctor_id"
                                                    :appointment_id = "a.appointment_id"
                                                    @success="successHandler"
                                                    @error="errorHandler"/>
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
                        <h3 class = "mb-3">Past Appointments</h3>
                        <div v-if = "patient.past_appointment.length == 0">
                            <p>No past appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in patient.past_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5> 
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <button class = "btn btn-outline-secondary">
                                                <RouterLink :to='`/doctor/appointment/${a.appointment_id}`' style="color: black; text-decoration: none;">
                                                    View Details
                                                </RouterLink>
                                            </button>
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
    import RescheduleAppointmentModal from '@/components/DoctorDashComp/RescheduleAppointmentModal.vue';

    export default {
        name: "DoctorDashViewPatient",
        data() {
            return {
                patient: null,
                ua: false,
                pa: false,
                errorMessage: "",
                successMessage: ""
            }
        },
        components: {
            errorToast,
            successToast,
            RescheduleAppointmentModal
        },
        methods: {
            async getPatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const display_patient = await requestAPI("GET", null, `/patient/${patientID}?past_appointment=true&upcoming_appointment=true`)
                    this.patient = display_patient
                }
                catch(error) {
                    this.errorHandler(error.message);
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getPatient()
                    this.successHandler("Appointment cancelled successfully!")
                }
                catch(error) {
                    this.errorHandler(error.message);
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
                this.getPatient()
                this.successMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.successMessage = '';
                }, 5000);
            },
        },
        mounted() {
            this.getPatient()
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>