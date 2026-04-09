<template>
    <div class = 'container w-75 mx-auto mb-3 px-0' v-bind="$attrs">
        <div class = "d-flex justify-content-between">
            <h2>Appointments</h2>

            <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#bookAppointment">
                Book Appointment
            </button>
        </div>
    </div>

    <!-- Add appointment  -->
    <BookAppointmentModal @error="handleModalError" @success="handleModalSuccess"/>

    <div class = "w-75 mx-auto" v-if="appointments">
        <div class = "d-flex justify-content-evenly mb-3">
            <a :class = "{'text-center link-dark appt-button w-50 pb-2': true, 'appt-button-active': ua == true}" @click = "ua = true">Upcoming Appointments</a>
            <a :class = "{'text-center link-dark appt-button w-50 pb-2': true, 'appt-button-active': ua == false}" @click = "ua = false">Past Appointments</a>
        </div>
    
        <!-- Upcoming appointments  -->
        <div v-show="ua">
            <!-- <h4>Upcoming Appointments</h4> -->
            <div v-if="appointments.upcoming_appointments && appointments.upcoming_appointments.length == 0">
                <p class = "px-4">No appointments to show</p>
            </div>

            <div v-else class = "d-flex justify-content-between align-items-center flex-wrap gap-4 mb-3">
                <div v-for="a in appointments.upcoming_appointments">
                    <div class="card" style="min-height: 220px; width: 222px;">
                        <div class="card-body">
                            <h5 class="card-title">{{ a.app_patient.name }}</h5>
                            <h6 class = "card-title">Dr. {{ a.app_doctor.name }}</h6>
                            <div class = "border-top">
                                <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p>
                                <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p>  
                                <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>                      
                                <div class = "d-flex gap-2" v-if="a.status == 'Booked'">
                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div> 
        </div>       

        <!-- Past appointments  -->
        <div v-show="!ua">
            <!-- <h4 id = 'past-appointments'>Past Appointments</h4> -->
            <div v-if="appointments.past_appointments && appointments.past_appointments.length == 0">
                <p class = "px-4">No appointments to show</p>
            </div>

            <div v-else class = "d-flex justify-content-between align-items-center flex-wrap gap-2 appointments">
                <div v-for="a in appointments.past_appointments">
                    <div class="card" style="min-height: 220px; width: 222px;">
                        <div class="card-body">
                            <h5 class="card-title">{{ a.app_patient.name }}</h5>
                            <h6 class = "card-title">Dr. {{ a.app_doctor.name }}</h6>
                            <div class = "border-top">
                                <p class="card-text mt-2 mb-2"><strong>ID: </strong>{{ a.appointment_id }}</p>
                                <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p>                        
                                <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                <RouterLink to=''>
                                    <button class = "btn btn-outline-secondary">View Details</button>
                                </RouterLink>
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

    import BookAppointmentModal from './BookAppointmentModal.vue';

    export default {
        name: 'AdminDashAppointment',
        emits: ['error', 'success'],
        data() {
            return {
                appointments: [],
                patient: null,
                doctor: null,
                all_patients: null,
                all_doctors: null,
                shift: null, 
                slot: null,
                ua: true,
                // pa: null
            }
        }, 
        components: {
            BookAppointmentModal
        },
        methods: {
            async PopulateAppointments() {
                try {
                    const all_appointments = await requestAPI('GET', null, '/appointments')
                    this.appointments = all_appointments
                }
                catch(error) {
                    this.$emit('error', error.message) 
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.PopulateAppointments()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            handleModalError(message) {
                this.$emit('error', message);
            },
            handleModalSuccess(message) {
                this.PopulateAppointments()
                this.$emit('success', message);
            },
        },
        mounted() {
            this.PopulateAppointments()
        }
    }
</script>

<style>
    .appt-button {
        /* border: 2px solid #ffb59b !important; */
        /* color: orangered;   */
        border-radius: 0 !important; 
        text-decoration: none !important;
    }
    
        
    .appt-button-active {
        /* background-color: #ff703c !important;
        color: white; */
        border-bottom: 2px solid orangered !important;

    }
</style>