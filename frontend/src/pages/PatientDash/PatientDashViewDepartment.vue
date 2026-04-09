<template>
    <div class="container d-flex align-items-center justify-content-center flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div v-if="dept" class = "container">
            <div class = "col">
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist">
                    <button class="nav-link active border-bottom" id="v-tab-upcoming-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-upcoming-appointment" type="button" role="tab">
                        Upcoming Appointments ({{ dept.upcoming_appointment.length }})
                    </button>

                    <button class="nav-link border-bottom" id="v-tab-past-appointment-tab" data-bs-toggle="pill" data-bs-target="#v-tab-past-appointment" type="button" role="tab">
                        Past Appointments ({{ dept.past_appointment.length }})
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
                        <h2>Department of {{ dept.name }}</h2>
                    </div>
                </div>

                <!-- Always visible  -->
                <div class = "container">
                    <div class = "row">
                        <!-- photo container  -->
                        <div class = 'col-sm-3 d-flex justify-content-center align-items-center'>
                            <div class = "d-flex flex-column justify-content-center align-items-center">
                                <div>
                                    <img :src="`/images/${dept.pfp}.png`" height="200px">
                                </div>
                            </div>
                        </div>

                        <!-- information container -->
                        <div class = 'col-9 p-3'>
                            <p><strong>Description: </strong>{{ dept.description }}</p>
                            <p><strong>Doctors: </strong></p>
                            <div>
                                <ul>
                                    <li v-for="doc in dept.doctors">Dr. {{ doc.name }}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1 mt-3" id="v-tab-tabContent">
                    
                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade show active w-100" id="v-tab-upcoming-appointment" role="tabpanel">
                        <h3 class = "mb-3">Upcoming Appointments</h3>
                        <div v-if = "dept.upcoming_appointment.length == 0">
                            <p>No upcoming appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <!-- Upcoming Appointments  -->
                            <div v-for="a in dept.upcoming_appointment">
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
                        <h3 class = "mb-3">Past Appointments</h3>
                        <div v-if = "dept.past_appointment.length == 0">
                            <p>No past appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in dept.past_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5> 
                                        <div class = "border-top">
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
        name: "PatientDashViewDepartment",
        data() {
            return {
                dept: null,
                ua: false,
                pa: false,
                errorMessage: "",
                successMessage: "",
            }
        },
        components: {
            errorToast,
            successToast,
            RescheduleAppointmentModal
        },
        methods: {
            async getDepartment() {
                try {
                    const deptID = this.$route.params.deptId;
                    const display_dept = await requestAPI("GET", null, `/dept/${deptID}?past_appointment=true&upcoming_appointment=true`)
                    this.dept = display_dept
                }
                catch(error) {
                    this.errorHandler(error.message);
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
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
                this.getDepartment()
                this.successMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.successMessage = '';
                }, 5000);
            },
        },
        mounted() {
            this.getDepartment()
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>