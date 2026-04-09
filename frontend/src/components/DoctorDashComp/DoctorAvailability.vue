<template>
    <div class="container d-flex flex-column align-items-start justify-content-between flex-grow-1 min-vh-90 min-vw-90 gap-3">
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#availModel">
            Provide Availability
        </button>
        <!-- modal  -->
        <AvailabilityModal @error = "handleModalError" @success="handleModalSuccess"/>

        <h4>Today's Appointments ({{ todayAppt.length }})</h4>
        <div v-if = "todayAppt.length == 0">
            <p>No appointments scheduled today</p>
        </div>

        <div class = "d-flex justify-content-start flex-wrap  gap-2">
            <div v-for="a in todayAppt">
                <div class="card" style="min-height: 220px; max-width: 222px;">
                    <div class="card-body">
                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                        <div class = "border-top">
                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                            <div v-if="a.status == 'Booked'">
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

                                    <button class="btn btn-outline-primary" data-bs-toggle="modal" :data-bs-target="`#rescheduleAppointment-${a.appointment_id}`">
                                            Reschedule
                                    </button>

                                    <!-- modal  -->
                                        <RescheduleAppointmentModal 
                                        :patient_id = "a.app_patient.patient_id"
                                        :doctor_id = "a.app_doctor.doctor_id"
                                        :appointment_id = "a.appointment_id"
                                        @success="handleModalSuccess"
                                        @error="handleModalError"/>
                                </div>
                            </div>

                            <div v-if="a.status == 'Completed'">
                                <RouterLink :to='`/doctor/appointment/${a.appointment_id}`'>
                                    <button class = "btn btn-outline-secondary">View Details</button>
                                </RouterLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <h4>This Week's Appointments ({{ thisWeekAppt.length }})</h4>
        <div v-if = "thisWeekAppt.length == 0">
            <p>No appointments scheduled this week</p>
        </div>

        <div class = "d-flex justify-content-start flex-wrap  gap-2">
            <div v-for="a in thisWeekAppt">
                <div class="card" style="min-height: 220px; max-width: 222px;">
                    <div class="card-body">
                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                        <div class = "border-top">
                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p>  
                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>                      
                            <div class = "d-flex gap-2" v-if="a.status == 'Booked'">
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
                                    @success="handleModalSuccess"
                                    @error="handleModalError"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <h4>Past Appointments ({{ pastAppt.length }})</h4>
        <div v-if = "pastAppt.length == 0">
            <p>No appointments scheduled to show</p>
        </div>

        <div class = "d-flex justify-content-start flex-wrap  gap-2">
            <div v-for="a in pastAppt">
                <div class="card" style="min-height: 220px; width: 222px;">
                    <div class="card-body">
                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                        <div class = "border-top">
                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p>                        
                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                            <RouterLink :to='`/doctor/appointment/${a.appointment_id}`'>
                                <button class = "btn btn-outline-secondary">View Details</button>
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>        
    </div>
</template>

<script>
    import { useUserStore } from '@/stores/userStore';
    import { requestAPI } from '../../../utils/api';
    
    import AvailabilityModal from './AvailabilityModal.vue';
    import RescheduleAppointmentModal from './RescheduleAppointmentModal.vue';
    import OngoingAppointmentModal from './OngoingAppointmentModal.vue';

    export default {
        name: "DoctorAvailability",
        emits: ['error', 'success'],
        data() {
            return {
                store: useUserStore(), 
                doctor: null,
                todayAppt: [],
                thisWeekAppt: [],
                pastAppt: [],
                selected_appt: null
            }
        },
        components: {
            AvailabilityModal,
            RescheduleAppointmentModal,
            OngoingAppointmentModal
        },
        methods: {
            handleModalError(message) {
                this.$emit('error', message);
            },
            handleModalSuccess(message) {
                this.populateAppointments()
                this.$emit('success', message);
            },
            async populateAppointments() {
                try {
                    const doctorID = this.store.user.doctor_id
                    const appts = await requestAPI("GET", null, `/doctor/appointments/${doctorID}`)
                    this.todayAppt = appts.today
                    this.thisWeekAppt = appts.this_week
                    this.pastAppt = appts.past
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.populateAppointments()
                    this.$emit("success", "Appointment cancelled added successfully!")
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async giveTreatmentDetails(data) {
                const appointmentID = this.selected_appt;
                try{
                    const give_details = await requestAPI("POST", data, `/treatment/${appointmentID}`)
                    if (give_details) {
                        // Refresh data
                        this.populateAppointments()
                        this.selected_appt = null
                        this.$emit("success", "Treatment Details added successfully!")
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
        },
        mounted() {
            this.populateAppointments()
        }
    }
</script>