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
                
                <!-- Always visible -->
                <div class = 'container'>
                    <div class = "d-flex justify-content-between">
                        <h2>Doctor Profile</h2>

                        <div class = "d-flex gap-1">
                            <button class = "btn btn-primary" v-show = "blacklist_button" v-on:click="changeBlacklistStatus">Blacklist</button>
                            <button class = "btn btn-primary" v-show = "undo_blacklist_button" v-on:click="changeBlacklistStatus"> Undo Blacklist</button>
                            <button class = "btn btn-primary" type = "button" data-bs-toggle="modal" data-bs-target="#exampleModal">Update</button>
                            <button class = "btn btn-primary" v-on:click="deleteDoctor">Delete</button>
                        </div>
                    </div>

                    <div class = 'row'>
                        <div class = 'col-sm-3'>
                            <img src = '../../../assets/DefaultDepartment.png' height="200px" width="200px">
                        </div>
                        
                        <div class = 'col'>
                            <h3 v-show = "blacklist_status">This user is currently blacklisted</h3>
                            <h3>Dr. {{ doctor.name }}</h3>
                            <p><strong>Contact Number:</strong> {{ doctor.doctor_user.contact_number }}</p>
                            <p><strong>Gender:</strong> {{ doctor.gender }}</p>
                            <p><strong>Email:</strong> {{ doctor.doctor_user.email }}</p>
                            <p><strong>DOB:</strong> {{ doctor.dob }}</p>
                            <p><strong>Gender:</strong> {{ doctor.gender }}</p>
                            <p><strong>Description:</strong> {{ doctor.description }}</p>
                        </div>
                    </div>
                </div>

                <!-- Modal -->
                <div class="modal fade" id="exampleModal" tabindex="-1">
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
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-primary">Save changes</button>
                                </div>
                            </form>

                        </div>
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
                pa: false,
                name: null,
                gender: null,
                dob: null,
                contact_number: null, 
                email: null,
                blacklist_status: null,
                blacklist_button: null,
                undo_blacklist_button: null
            }
        },
        methods: {
            async getDoctor() {
                const doctorID = this.$route.params.did;
                const display_doctor = await requestAPI('GET', null, `/doctor/${doctorID}?past_appointment=true&upcoming_appointment=true&availability=true`)
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
                }
                catch(error) {
                    console.error('Error updating doctor:', error)
                }
            },

            async deleteDoctor() {
                try {
                    const doctorID = this.$route.params.did;
                    const delete_doctor = await requestAPI('DELETE', null, `/doctor/${doctorID}`)
                    console.log('deleted')
                }
                catch(error) {
                    console.error('Error deleting doctor:', error)
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
                    console.error("Error blacklisting doctor:", error)
                }
            }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>