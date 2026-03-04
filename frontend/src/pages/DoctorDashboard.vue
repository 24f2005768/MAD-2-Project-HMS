<template>
    <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container' v-if="doctor">
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist">
                    <button class="nav-link active border-bottom" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Home</button>
                    <button class="nav-link border-bottom" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Stats</button>
                    <button class="nav-link border-bottom" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Patients</button>
                    <button class="nav-link border-bottom" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">Appointments & Availability</button>
                </div>                
            </div>

            <div class = 'col'>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex" id="v-tab-tabContent" style="margin: 30px;">
                    
                    <!-- Home  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">

                        <!-- experiment -->
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
                                    <div>
                                        <h3>Department of {{ doctor.dept.name }}</h3>
                                        <p><strong>Appointments Today:</strong> {{ doctor.today_appointment.length }}</p>
                                        <p><strong>Appointments This Week:</strong> {{ doctor.upcoming_appointment.length }}</p>
                                        <p><strong>Patients: </strong>{{ doctor.number_of_patients }}</p>
                                    </div>
                                    <div class="ms-auto">
                                        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#view-profile">View Profile</button>
                                    </div>
                                </div>
                            </div>
                        </div>                        
                        


                        <!-- other information  -->
                        <div class = "m-4">
                            <h4>Your today's appointments</h4>

                            <div class = "d-flex justify-content-between flex-wrap  gap-2">
                                <div v-for="a in doctor.today_appointment">
                                    <div class="card">
                                        <div class="card-body">
                                            <h5 class="card-title">{{ a.app_patient.name }}</h5>
                                            <p class="card-text"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <div class = "d-flex gap-2">
                                                <button class = "btn btn-primary">Cancel</button>
                                                <button class = "btn btn-primary">Reschedule</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <!-- Stats -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        Second
                    </div>

                    <!-- Patients  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <DoctorDashPatients />
                    </div>

                    <!-- Availability and Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#availModel">
                        Availability
                        </button>
                        
                        <AvailabilityModal />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../utils/api';
    import AvailabilityModal from '@/components/DoctorDashComp/AvailabilityModal.vue';
    import DoctorDashPatients from '@/components/DoctorDashComp/DoctorDashPatients.vue';
    import errorToast from '@/components/errorToast.vue';
    import { useUserStore } from '@/stores/userStore';
    
    export default {
        name: 'DoctorDash',
        data() {
            return {
                doctor: null,
                errorMessage: "",
                store: useUserStore()
            }
        },
        components: {
            AvailabilityModal,
            DoctorDashPatients,
            errorToast
        },
        methods: {
            async getDoctor() {
                try {
                    console.log("user", this.store.user)
                    const doctorID = this.store.user.doctor_id;
                    const display_doctor = await requestAPI('GET', null, `/doctor/${doctorID}?past_appointment=true&upcoming_appointment=true&availability=true&today_appointment=true`)
                    this.doctor = display_doctor
                }
                catch(error) {
                    this.errorHandler(error.message);
                }
            },
            errorHandler(message) {
                this.errorMessage = message;
                }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        /* background-color: rgba(0, 0, 0, 0.175) !important; */
        border-bottom: 2px solid orangered !important;
    }
</style>