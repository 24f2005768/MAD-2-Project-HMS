<template>
    <div v-if="patient" v-bind="$attrs">
        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow rounded" style="background-color: #EEF6EF;">
            <!-- photo container  -->
            <div class = "col-3 d-flex flex-column justify-content-center align-items-center p-2">
                <div class = "rounded p-2 d-flex flex-column justify-content-center align-items-center">
                    <div class = "mt-2">
                        <img :src="`/images/${patient.pfp}.png`" height="150px">
                    </div>
                </div>
            </div>

            <!-- information container -->
            <div class = "col-9 d-flex align-items-center p-3">
                <!-- heading and update profile button  -->
                <div class = "d-flex justify-content-between w-100">
                    <div class="w-100">
                        <div class="d-flex justify-content-between mb-3">
                            <div>
                                <h4 class = "m-10">{{ patient.name }}</h4>
                            </div>

                            <div class = "d-flex gap-2">
                                <button v-if="!collapseProfile" class = "btn btn-outline-secondary" type="button" data-bs-toggle = "modal" data-bs-target = "#update-patient-profile-modal">
                                    Update
                                </button>

                                <!-- modal  -->
                                <PatientProfileUpdateModal v-if="patient" 
                                :patient = "patient" 
                                @update-profile="updatePatientProfile"/>

                                <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#view-profile" v-on:click="collapseProfile = !collapseProfile">
                                    <span v-if="collapseProfile">View Profile</span>
                                    <span v-else>Collapse Profile</span>
                                </button>
                            </div>
                        </div>
                                               
                        <p><strong>Appointments Today:</strong> {{ patient.today_appointment.length }}</p>
                        <p><strong>Appointments This Week:</strong> {{ patient.upcoming_appointment.length }}</p>
                        
                        <!-- collapse content -->
                        <div class = 'collapse' id = 'view-profile'>
                            <p><strong>Gender: </strong>{{ patient.gender }}</p>
                            <p><strong>DOB: </strong>{{ patient.dob }}</p>
                            <p><strong>Age: </strong>{{ patient.get_age }}</p>
                            <p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ patient.patient_user.email }}</p>
                            <p><strong>Height: </strong>{{ patient.height }}</p>
                            <p><strong>Weight: </strong>{{ patient.weight }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>                        
        
        <!-- other information  -->
        <div class = "m-4">
            <h4 class = "mb-4">Today's appointments ({{ patient.today_appointment.length }})</h4>
            <div v-if = "patient.today_appointment.length == 0">
                <p>No appointments scheduled today</p>
            </div>

            <div class = "d-flex justify-content-start flex-wrap gap-2">
                <div v-for="a in patient.today_appointment">
                    <div class="card" style="min-height: 220px; max-width: 222px;">
                        <div class="card-body">
                            <h5 class="card-title">Dr. {{ a.app_doctor.name }}</h5>
                            <div class = "border-top">
                                <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                <div v-if = "a.status == 'Booked'">                                   
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
                                    <!-- <RouterLink :to='`/doctor/appointment/${a.appointment_id}`'> -->
                                        <button class = "btn btn-outline-secondary">
                                            View Details
                                        </button>
                                    <!-- </RouterLink> -->
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

    import PatientProfileUpdateModal from './PatientProfileUpdateModal.vue';

    export default {
        name: "PatientProfile",
        data() {
            return {
                store: useUserStore(),
                patient: null,
                errorMessage: "",
                collapseProfile: true,
                selected_appt: null
            }
        },
        components: {
            PatientProfileUpdateModal
        },
        methods: {
            async getPatient() {
                try {
                    const patientID = this.store.user.patient_id;
                    const display_patient = await requestAPI('GET', null, `/patient/${patientID}?past_appointment=true&upcoming_appointment=true&today_appointment=true`)
                    this.patient = display_patient
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getPatient()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async updatePatientProfile(data) {
                try{
                    const patientID = this.store.user.patient_id;
                    const update_patient = await requestAPI('PATCH', data, `/patient/${patientID}`)
                    if (update_patient) {
                        // Refresh patient data
                        this.getPatient()
                    } 
                    // close modal
                    const modalEl = document.getElementById('update-patient-profile-modal');
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    modal.hide()
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        },
        mounted() {
            this.getPatient()
        }
    }
</script>