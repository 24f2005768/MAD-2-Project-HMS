<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Upcoming Appointments
                    </button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">
                        Past Appointments
                    </button>
                </div>                
            </div>

            <div v-if = "patient" class = 'col'>
                <div class="d-flex justify-content-end my-2">
                    <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>
                        Go Back
                    </button>
                </div>

                <div clas = "container">
                    <div class = "d-flex justify-content-between">
                        <h2>Patient Profile</h2>

                        <div class = "d-flex gap-2">
                            <button class = "btn btn-outline-danger" v-show = "blacklist_button" v-on:click="changeBlacklistStatus">
                                Blacklist
                            </button>

                            <button class = "btn btn-outline-danger" v-show = "undo_blacklist_button" v-on:click="changeBlacklistStatus">
                                Undo Blacklist
                            </button>
                            
                            <button class = "btn btn-outline-secondary" type = "button" data-bs-toggle = "modal" data-bs-target = "#update-patient-modal">
                                Update
                            </button>

                            <button class = "btn btn-outline-primary" v-on:click="deletePatient">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Modal  -->
                <div class = "modal fade" id = "update-patient-modal" tabindex = "-1">
                    <div class = "modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Update Patient Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <form @submit.prevent = "updatePatient">
                                <div class="modal-body">
                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "patient.name"
                                        id="floatingInput">
                                        <label for = "name" class = "form-label">Name</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <select v-model = "patient.gender" class="form-select">
                                            <option disabled value = "">Select Gender</option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                            <option value="Other">Other</option>
                                        </select>
                                        <label for = "gender" class="form-label">Gender</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "date" class = "form-control" v-model = "patient.dob"
                                        id="floatingInput">
                                        <label for = "dob" class = "form-label">DOB</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "patient.patient_user.contact_number"
                                        id="floatingInput">
                                        <label for = "contact_number" class = "form-label">Contact Number</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "patient.patient_user.email"
                                        id="floatingInput">
                                        <label for = "email" class = "form-label">Email</label>
                                    </div>


                                </div>
                                
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-outline-primary">Update Patient</button>
                                </div>
                            </form>
                        </div>                        
                    </div>
                </div>

                <!-- Always visible -->
                 <div class = 'container'>
                    <div class = 'row'>
                        <div class = 'col-sm-3 text-center'>
                            <img :src="`/images/${patient.pfp}.png`" height="200px" width="200px">
                            <p><strong>Name: </strong>{{ patient.name }}</p>
                        </div>
                        
                        <div class = 'col'>
                            <h3 v-show = "blacklist_status">This user is currently blacklisted</h3>
                            <p><strong>Patient ID: </strong> {{ patient.patient_id }}</p>
                            <p><strong>Gender: </strong>{{ patient.gender }}</p>
                            <p><strong>DOB: </strong>{{ patient.dob }}</p>
                            <p><strong>Age: </strong>{{ patient.get_age }}</p>
                            <p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ patient.patient_user.email }}</p>
                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade show active w-100 my-3" id="v-tab-home" role="tabpanel">
                        <h3 class = "my-3">Upcoming Appointments</h3>
                        <div v-if="patient.upcoming_appointment.length != 0 || patient.today_appointment.length != 0" class = "d-flex justify-content-start flex-wrap  gap-2">

                            <!-- Today's appointments  -->
                            <div v-for="a in patient.today_appointment">
                                <div class="card" style="height: 240px; width: 235px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Doctor: </strong>Dr. {{ a.app_doctor.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                            <div v-if="a.status == 'Booked'">
                                                <div class = "d-flex gap-2 mt-2">
                                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                                </div>
                                            </div>

                                            <div v-else-if="a.status == 'Completed'">
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

                            <!-- Upcoming Appointments  -->
                            <div v-for="a in patient.upcoming_appointment">
                                <div class="card" style="height: 240px; width: 235px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Doctor: </strong>Dr. {{ a.app_doctor.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                            <div v-if="a.status == 'Booked'">
                                                <div class = "d-flex gap-2 mt-2">
                                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                                </div>
                                            </div>

                                            <div v-else-if="a.status == 'Completed'">
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
                        </div>

                        <div v-else>
                            <p>No upcoming appointments to show</p>
                        </div>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100 my-3" id="v-tab-profile" role="tabpanel">
                        <h3 class = "my-3">Past Appointments</h3>

                        <div v-if="patient.past_appointment.length != 0" class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in patient.past_appointment">
                                <div class="card" style="height: 240px; width: 235px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5> 
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Doctor: </strong>Dr. {{ a.app_doctor.name }}</p>
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
        name: 'ViewPatient',
        data() {
            return {
                patient: null,
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
            async getPatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const display_patient = await requestAPI('GET', null, `/patient/${patientID}?past_appointment=true&upcoming_appointment=true&today_appointment=true`)
                    this.patient = display_patient

                     // if the patient is blacklisted, show the undo_blacklist_button
                    if (this.patient.patient_user.blacklisted == true) {
                        this.blacklist_status = true
                        this.blacklist_button = false
                        this.undo_blacklist_button = true
                    }
                    // if the patient is not blacklisted, show the blacklist_button
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

            async updatePatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const data = {
                        name: this.patient.name,
                        gender: this.patient.gender,
                        dob: this.patient.dob,
                        email: this.patient.patient_user.email,
                        contact_number: this.patient.patient_user.contact_number
                    }

                    const update_patient = await requestAPI('PATCH', data, `/patient/${patientID}`)
                    this.successHandler("Patient updated successfully")
                    bootstrap.Modal.getInstance(document.getElementById('update-patient-modal')).hide()
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async deletePatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const delete_patient = await requestAPI('DELETE', null, `/patient/${patientID}`)
                    this.$router.push("/admin")
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },
            async changeBlacklistStatus() {
                try {
                    const patientID = this.$route.params.pid;
                    const data = {
                        blacklist: this.patient.patient_user.blacklisted
                    }
                    console.log(data)
                    const changestatus = await requestAPI("PATCH", data, `/patient/${patientID}`)
                    this.getPatient()
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
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