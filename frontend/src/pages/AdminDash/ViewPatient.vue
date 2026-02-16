<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Upcoming Appointments</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Past Appointments</button>
                </div>                
            </div>

            <div v-if = "patient" class = 'col'>
                <div clas = "container">
                    <div class = "d-flex justify-content-between">
                        <h2>Patient Profile</h2>

                        <div class = "d-flex gap-1">
                            
                            <button class = "btn btn-primary">
                                Blacklist
                            </button>
                            
                            <button class = "btn btn-primary" type = "button" data-bs-toggle = "modal" data-bs-target = "#update-patient-modal">
                                Update
                            </button>

                            <button class = "btn btn-primary" v-on:click="deletePatient">
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
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-primary">Save changes</button>
                                </div>
                            </form>
                        </div>                        
                    </div>
                </div>

                <!-- Always visible -->
                 <div class = 'container'>
                    <div class = 'row'>
                        <div class = 'col-sm-3'><img src = '../../../assets/DefaultDepartment.png' height="200px" width="200px"></div>
                        <div class = 'col'>
                            <p><strong>Name: </strong>{{ patient.name }}</p>
                            <p><strong>Patient ID: </strong> {{ patient.patient_id }}</p>
                            <p><strong>Gender: </strong>{{ patient.gender }}</p>
                            <p><strong>DOB: </strong>{{ patient.dob }}</p>
                            <p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ patient.patient_user.email }}</p>
                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <h3>Upcoming Appointments</h3>
                        <div v-if = "ua">
                            <ol>
                                <li v-for = "a in patient.upcoming_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Date:</strong> {{ a.date }}</p>
                                    <p><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                    <p><strong>Doctor:</strong> {{ a.app_doctor.name }}</p>
                                </li>
                            </ol>                            
                        </div>
                        <p v-else>No upcoming appointments to show</p>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <h3>Past Appointments</h3>
                        <div v-if = "pa">
                            <ol>
                                <li v-for = "a in patient.past_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Date:</strong> {{ a.date }}</p>
                                    <p><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                    <p><strong>Patient:</strong> {{ a.app_doctor.name }}</p>
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
        name: 'ViewPatient',
        data() {
            return {
                patient: null,
                ua: false,
                pa: false,
                name: null,
                gender: null,
                dob: null,
                contact_number: null, 
                email: null

            }
        },
        methods: {
            async getPatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const display_patient = await requestAPI('GET', null, `/patient/${patientID}?past_appointment=true&upcoming_appointment=true`)
                    this.patient = display_patient

                    // check if there are any upcoming appointments
                    if (this.patient.upcoming_appointment.length != 0) {
                        this.ua = true
                    }

                    // check if there are any past appointments
                    if (this.patient.past_appointment.length != 0) {
                        this.pa = true
                    }
                }
                catch(error) {
                    console.error('Error displaying patient:', error)                    
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
                }
                catch(error) {
                    console.error('Error updating patient:', error)
                }
            },

            async deletePatient() {
                try {
                    const patientID = this.$route.params.pid;
                    const delete_patient = await requestAPI('DELETE', null, `/patient/${patientID}`)
                    console.log('deleted')
                }
                catch(error) {
                    console.error('Error deleting patient:', error)
                }
            }
        },
        mounted() {
            this.getPatient()
        }
    }
</script>