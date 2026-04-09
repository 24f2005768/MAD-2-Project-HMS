<template>
    <div class = "my-3">
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#bookAppointment">
            Book Appointment
        </button>
    </div>

    <!-- modal  -->
     <BookAppointmentModal @success="handleModalSuccess"/>

        <h4>Today's Appointments ({{ todayAppt.length }})</h4>
        <div v-if = "todayAppt.length == 0">
            <p>No appointments scheduled today</p>
        </div>

        <div class = "d-flex justify-content-start flex-wrap  gap-2">
            <div v-for="a in todayAppt">
                <div class="card" style="min-height: 220px; max-width: 222px;">
                    <div class="card-body">
                        <h5 class="card-title">Dr. {{ a.app_doctor.name }}</h5>
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
                                    :doctor_id = "a.app_doctor.doctor_id"
                                    :appointment_id = "a.appointment_id"
                                    @success="handleModalSuccess"
                                    @error="handleModalError"/>
                                </div>
                            </div>

                            <div v-if="a.status == 'Completed'">
                                <RouterLink :to='`/patient/appointment/${a.appointment_id}`'>
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
                        <h5 class="card-title">Dr. {{ a.app_doctor.name }}</h5>
                        <div class = "border-top">
                            <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p>
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
                        <h5 class="card-title">Dr. {{ a.app_doctor.name }}</h5>
                        <div class = "border-top">
                            <p class="card-text mt-2 mb-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p>
                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p>                        
                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                            <RouterLink :to='`/patient/appointment/${a.appointment_id}`'>
                                <button class = "btn btn-outline-secondary">View Details</button>
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>        

</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    import BookAppointmentModal from './BookAppointmentModal.vue';
    import RescheduleAppointmentModal from './RescheduleAppointmentModal.vue';

    export default {
        name: 'PatientDashAppointments',
        emits: ['error', 'success'],
        data() {
            return {
                store: useUserStore(),
                all_doctors: null,
                appts: null,
                todayAppt: [],
                thisWeekAppt: [],
                pastAppt: []
            }
        }, 
        components: {
            BookAppointmentModal,
            RescheduleAppointmentModal
        },
        methods: {
            // async PopulatePatientsDoctors() {
            //     const allDoctors = await requestAPI("GET", null, "/doctors")
            //     this.all_doctors = allDoctors
            // },
            async populateAppointments() {
                try {
                    const patientID = this.store.user.patient_id
                    const appts = await requestAPI("GET", null, `/patient/${patientID}?today_appointment=true&upcoming_appointment=true&past_appointment=true`)
                    this.todayAppt = appts.today_appointment
                    this.thisWeekAppt = appts.upcoming_appointment
                    this.pastAppt = appts.past_appointment
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.populateAppointments()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            handleModalError(message) {
                this.$emit('error', message);
            },
            handleModalSuccess(message) {
                this.populateAppointments()
                this.$emit('success', message);
            },
        },
        mounted() {
            this.populateAppointments()
        }
    }
</script>