<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Availability
                    </button>

                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">
                        Upcoming Appointments
                    </button>

                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">
                        Past Appointments
                    </button>
                </div>                
            </div>

            <div v-if="doctor" class = 'col'>
                
                <!-- Always visible -->
                <div class = 'container'>
                    <div class = "d-flex justify-content-between">
                        <h2>Doctor Profile</h2>

                        <div class = "d-flex gap-1">
                            <button class = "btn btn-outline-danger" v-show = "blacklist_button" v-on:click="changeBlacklistStatus">
                                Blacklist
                            </button>

                            <button class = "btn btn-outline-danger" v-show = "undo_blacklist_button" v-on:click="changeBlacklistStatus">
                                Undo Blacklist
                            </button>
                            
                            <button class = "btn btn-outline-secondary" type = "button" data-bs-toggle = "modal" data-bs-target = "#update-doctor-modal">
                                Update
                            </button>

                            <button class = "btn btn-outline-primary" v-on:click="deleteDoctor">
                                Delete
                            </button>
                        </div>
                    </div>

                    <div class = 'row'>
                        <div class = 'col-sm-3 text-center'>
                            <img :src="`/images/${doctor.pfp}.png`" height="200px" width="200px">
                            <h3>Dr. {{ doctor.name }}</h3>
                        </div>
                        
                        <div class = 'col'>
                            <h3 v-show = "blacklist_status">This user is currently blacklisted</h3>
                            <p><strong>Doctor ID:</strong> {{ doctor.doctor_id }}</p>
                            <p><strong>Contact Number:</strong> {{ doctor.doctor_user.contact_number }}</p>
                            <p><strong>Email:</strong> {{ doctor.doctor_user.email }}</p>
                            <p><strong>DOB:</strong> {{ doctor.dob }}</p>
                            <p><strong>Gender:</strong> {{ doctor.gender }}</p>
                            <p><strong>Description:</strong> {{ doctor.description }}</p>
                        </div>
                    </div>
                </div>

                <!-- Modal -->
                <div class="modal fade" id="update-doctor-modal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Update Doctor Details</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <form @submit.prevent = "updateDoctor">
                                <div class="modal-body">
                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "doctor.name"
                                        id="floatingInput">
                                        <label for = "name" class = "form-label">Name</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <select v-model = "doctor.gender" class="form-select">
                                            <option disabled value = "">Select Gender</option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                            <option value="Other">Other</option>
                                        </select>
                                        <label for = "gender" class="form-label">Gender</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "date" class = "form-control" v-model = "doctor.dob"
                                        id="floatingInput">
                                        <label for = "dob" class = "form-label">DOB</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "doctor.doctor_user.contact_number"
                                        id="floatingInput">
                                        <label for = "contact_number" class = "form-label">Contact Number</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "doctor.doctor_user.email"
                                        id="floatingInput">
                                        <label for = "email" class = "form-label">Email</label>
                                    </div>
                                </div>
                                
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-outline-primary">Update Doctor</button>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Availability  -->
                    <div class="tab-pane fade show active w-100 mt-3" id="v-tab-home" role="tabpanel">
                        <table class = "w-75 mx-auto table table-striped table-hover table-bordered">
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
                       <!-- card for each appointment  -->
                        <div v-if="doctor.upcoming_appointment.length != 0 || doctor.today_appointment.length != 0" class = "d-flex justify-content-start flex-wrap  gap-2">
                            <!-- Today's appointments -->
                            <div v-for="a in doctor.today_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                                        <!-- <h6 class = "card-title">Dr. {{ a.app_doctor.name }}</h6> -->
                                        <div class = "border-top">
                                            <p class="card-text mb-2 mt-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p> 
                                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p> 
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <button v-if="a.status == 'Booked'" class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-for="a in doctor.upcoming_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                                        <!-- <h6 class = "card-title">Dr. {{ a.app_doctor.name }}</h6> -->
                                        <div class = "border-top">
                                            <p class="card-text mb-2 mt-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p> 
                                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p> 
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <button v-if="a.status == 'Booked'" class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                        <div v-else>
                            <p>No upcoming appointments to show</p>
                        </div>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <!-- card for each appointment  -->
                        <div v-if="doctor.past_appointment.length != 0" class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in doctor.past_appointment">
                                <div class="card" style="min-height: 220px; max-width: 222px;">
                                    <div class="card-body">
                                        <h5 class="card-title">{{ a.app_patient.name }}</h5>
                                        <!-- <h6 class = "card-title">Dr. {{ a.app_doctor.name }}</h6> -->
                                        <div class = "border-top">
                                            <p class="card-text mb-2 mt-2"><strong>Appt. ID: </strong>{{ a.appointment_id }}</p> 
                                            <p class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</p> 
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <button class = "btn btn-outline-secondary">
                                                <RouterLink :to = '`/admin/appointment/${a.appointment_id}`' style="color: black; text-decoration: none;">
                                                    View Details
                                                </RouterLink>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-else>
                            <p>No past appointments to show</p>
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
    
    export default {
        name: 'ViewDoctor',
        emits: ['error', 'success'],
        data() {
            return {
                doctor: null, 
                ua: false,
                pa: false,
                name: null,
                gender: null,
                dob: null,
                contact_number: null, 
                email: null,
                blacklist_status: null,
                blacklist_button: null,
                undo_blacklist_button: null,
                errorMessage: null,
                successMessage: null
            }
        },
        components: {
            errorToast,
            successToast
        },
        methods: {
            async getDoctor() {
                try {
                    const doctorID = this.$route.params.did;
                    const display_doctor = await requestAPI('GET', null, `/doctor/${doctorID}?past_appointment=true&upcoming_appointment=true&today_appointment=true&availability=true`)
                    this.doctor = display_doctor
                    
                    // check if there are any upcoming appointments
                    if (this.doctor.upcoming_appointment.length != 0) {
                        this.ua = true
                    }

                    // check if there are any past appointments
                    if (this.doctor.past_appointment.length != 0) {
                        this.pa = true
                    }

                    // if the doctor is blacklisted, show the undo_blacklist_button
                    if (this.doctor.doctor_user.blacklisted == true) {
                        this.blacklist_status = true
                        this.blacklist_button = false
                        this.undo_blacklist_button = true
                    }
                    // if the doctor is not blacklisted, show the blacklist_button
                    else {
                        this.blacklist_status = false
                        this.blacklist_button = true
                        this.undo_blacklist_button = false
                    }
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async updateDoctor() {
                try {
                    const doctorID = this.$route.params.did;
                    const data = {
                        name: this.doctor.name,
                        gender: this.doctor.gender,
                        dob: this.doctor.dob,
                        email: this.doctor.doctor_user.email,
                        contact_number: this.doctor.doctor_user.contact_number
                    }

                    const update_doctor = await requestAPI('PATCH', data, `/doctor/${doctorID}`)
                    this.successMessage =  "Doctor updated successfully"
                    bootstrap.Modal.getInstance(document.getElementById('update-doctor-modal')).hide()
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async deleteDoctor() {
                try {
                    const doctorID = this.$route.params.did;
                    const delete_doctor = await requestAPI('DELETE', null, `/doctor/${doctorID}`)
                    this.successHandler("Doctor deleted successfully!")
                    this.$router.push("/admin")
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async changeBlacklistStatus() {
                try {
                    const doctorID = this.$route.params.did;
                    const data = {
                        blacklist: this.doctor.doctor_user.blacklisted
                    }
                    console.log(data)
                    const changestatus = await requestAPI("PATCH", data, `/doctor/${doctorID}`)
                    this.getDoctor()
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getDoctor()
                    this.successHandler("Appointment cancelled successfully!")
                }
                catch(error) {
                    this.errorHandler(error.message)
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
                this.getDoctor()
                this.successMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.successMessage = '';
                }, 5000);
            },
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>