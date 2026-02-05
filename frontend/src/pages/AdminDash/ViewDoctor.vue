<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Availability</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Upcoming Appointments</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Past Appointments</button>
                </div>                
            </div>

            <div v-if="doctor" class = 'col'>
                <h2>Dr. {{ doctor.name }}'s Profile</h2>

                <!-- Always visible -->
                <div class = 'container'>
                    <div class = 'row'>
                        <div class = 'col-sm-3'><img src = '../../../assets/DefaultDepartment.png' height="200px" width="200px"></div>
                        <div class = 'col'>{{ doctor.description }}</div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Availability  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <table class = "table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Shift Name</th>
                                    <th>Shift Time</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "s in doctor.availability">
                                    <th>{{ s.date }}</th>
                                    <th>{{ s.name }}</th>
                                    <th>{{ s.start_time }} - {{ s.end_time }}</th>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <div v-if = "ua">
                            <ol>
                                <li v-for = "a in doctor.upcoming_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Date:</strong> {{ a.date }}</p>
                                    <p><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                    <p><strong>Patient:</strong> {{ a.app_patient.name }}</p>
                                </li>
                            </ol>                            
                        </div>
                        <p v-else>No upcoming appointments to show</p>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <div v-if = "pa">
                            <ol>
                                <li v-for = "a in doctor.past_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Date:</strong> {{ a.date }}</p>
                                    <p><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                    <p><strong>Patient:</strong> {{ a.app_patient.name }}</p>
                                </li>
                            </ol>                            
                        </div>
                        <p v-else>No past appointments to show</p>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    
    export default {
        name: 'ViewDoctor',
        data() {
            return {
                doctor: null, 
                ua: false,
                pa: false
            }
        },
        methods: {
            async getDoctor() {
                const doctorId = this.$route.params.did;
                const display_doctor = await requestAPI('GET', null, `/doctor/${doctorId}?past_appointment=true&upcoming_appointment=true&availability=true`)
                this.doctor = display_doctor
                
                // check if there are any upcoming appointments
                if (this.doctor.upcoming_appointment.length != 0) {
                    this.ua = true
                }

                // check if there are any past appointments
                if (this.doctor.past_appointment.length != 0) {
                    this.pa = true
                }
            }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>