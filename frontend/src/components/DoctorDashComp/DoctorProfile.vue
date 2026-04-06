<template>
    <div v-if="doctor" v-bind="$attrs">
        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow rounded" style="background-color: #EEF6EF;">
            <!-- photo container  -->
            <div class = "col-3 d-flex flex-column justify-content-center align-items-center p-2">
                <div class = "rounded p-2 d-flex flex-column justify-content-center align-items-center">
                    <div class = "mt-2">
                        <img :src="`/images/${doctor.pfp}.png`" height="150px">
                    </div>

                    <div>
                        <h3 class = "m-10">Dr. {{ doctor.name }}</h3>
                    </div>
                </div>
            </div>

            <!-- information container -->
            <div class = "col-9 d-flex align-items-center p-3">
                <!-- heading and update profile button  -->
                <div class = "d-flex justify-content-between w-100">
                    <div class="w-100">
                        <div class="d-flex justify-content-between mb-3">
                            <h3>Department of {{ doctor.dept.name }}</h3>
                            <div class = "d-flex gap-2">
                                <button v-if="!collapseProfile" class = "btn btn-outline-secondary" type="button" data-bs-toggle = "modal" data-bs-target = "#update-doctor-profile-modal">
                                    Update
                                </button>

                                <!-- modal  -->
                                <DoctorProfileUpdateModal v-if="doctor" 
                                :doctor = "doctor" 
                                @update-profile="updateDoctorProfile"/>

                                <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#view-profile" v-on:click="collapseProfile = !collapseProfile">
                                    <span v-if="collapseProfile">View Profile</span>
                                    <span v-else>Collapse Profile</span>
                                </button>

                                <button class = "btn btn-outline-info" @click="sendMonthlyReport">
                                    Request Monthly Report
                                </button>
                            </div>
                        </div>
                        
                        <p><strong>Appointments Today:</strong> {{ doctor.today_appointment.length }}</p>
                        <p><strong>Appointments This Week:</strong> {{ doctor.upcoming_appointment.length }}</p>
                        <p><strong>Patients: </strong>{{ doctor.number_of_patients }}</p>
                        
                        <!-- collapse content -->
                        <div class = 'collapse' id = 'view-profile'>
                            <p><strong>Gender: </strong>{{ doctor.gender }}</p>
                            <p><strong>DOB: </strong>{{ doctor.dob }}</p>
                            <p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p>
                            <p><strong>Description: </strong>{{ doctor.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>                        
        
        <!-- other information  -->
        <div class = "m-4">
            <h4 class = "mb-4">Today's appointments ({{ doctor.today_appointment.length }})</h4>
            <div v-if = "doctor.today_appointment.length == 0">
                <p>No appointments scheduled today</p>
            </div>

            <div class = "d-flex justify-content-start flex-wrap gap-2">
                <div v-for="a in doctor.today_appointment">
                    <div class="card" style="min-height: 220px; max-width: 222px;">
                        <div class="card-body">
                            <h5 class="card-title">{{ a.app_patient.name }}</h5>
                            <div class = "border-top">
                                <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                <div v-if = "a.status == 'Booked'">
                                    <button class = "btn btn-outline-secondary" data-bs-toggle="modal" :data-bs-target="`#ongoing-appt-modal-${a.appointment_id}`" v-on:click="selected_appt = a.appointment_id">
                                        Provide Details
                                    </button>
                                    
                                    <!-- Modal  -->
                                    <OngoingAppointmentModal 
                                    :appointmentID="a.appointment_id"
                                    @treatment="giveTreatmentDetails" />

                                    <div class = "d-flex gap-2 mt-2">
                                        <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">
                                            Cancel
                                        </button>

                                        <button class = "btn btn-outline-primary">
                                            Reschedule
                                        </button>
                                    </div>
                                </div>

                                <div v-if = "a.status == 'Completed'">
                                    <RouterLink :to='`/doctor/appointment/${a.appointment_id}`'>
                                        <button class = "btn btn-outline-secondary">
                                            View Details
                                        </button>
                                    </RouterLink>
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
    import { useUserStore } from '@/stores/userStore';


    import DoctorProfileUpdateModal from './DoctorProfileUpdateModal.vue';
    import OngoingAppointmentModal from './OngoingAppointmentModal.vue';

    export default {
        name: "DoctorProfile",
        data() {
            return {
                store: useUserStore(),
                doctor: null,
                errorMessage: "",
                collapseProfile: true,
                selected_appt: null
            }
        },
        components: {
            DoctorProfileUpdateModal,
            OngoingAppointmentModal
        },
        methods: {
            async getDoctor() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const display_doctor = await requestAPI('GET', null, `/doctor/${doctorID}?past_appointment=true&upcoming_appointment=true&availability=true&today_appointment=true`)
                    this.doctor = display_doctor
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getDoctor()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async updateDoctorProfile(data) {
                try{
                    const doctorID = this.store.user.doctor_id;
                    const update_doctor = await requestAPI('PATCH', data, `/doctor/${doctorID}`)
                    if (update_doctor) {
                        // Refresh doctor data
                        this.getDoctor()
                    } 
                    // close modal
                    const modalEl = document.getElementById('update-doctor-profile-modal');
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    modal.hide()
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
            async giveTreatmentDetails(data) {
                const appointmentID = this.selected_appt;
                try{
                    const give_details = await requestAPI("POST", data, `/treatment/${appointmentID}`)
                    if (give_details) {
                        // Refresh doctor data
                        this.getDoctor()
                        this.selected_appt = null
                    } 
                    // close modal
                    const modalEl = document.getElementById(`ongoing-appt-modal-${appointmentID}`);
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    console.log(modal)
                    modal.hide()
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
            async sendMonthlyReport() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const send_history = await requestAPI("GET", null, `/doctor/monthly-report/${doctorID}`)

                    if (send_history) {
                        this.$emit('success', "Your report was sent successfully! Please check your inbox.")
                    }
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>