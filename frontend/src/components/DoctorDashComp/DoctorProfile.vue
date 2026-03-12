<template>
    <div v-if="doctor" v-bind="$attrs">
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
                    <div class="w-100">
                        <div class="d-flex justify-content-between mb-3">
                            <h3>Department of {{ doctor.dept.name }}</h3>
                            <div class = "d-flex gap-2">
                                <button v-if="!collapseProfile" class = "btn btn-outline-secondary" type="button" data-bs-toggle = "modal" data-bs-target = "#update-doctor-profile-modal">
                                    Update
                                </button>

                                <!-- modal  -->
                                 <!-- <DoctorProfileUpdateModal /> -->

                                <div v-if="doctor" class = "modal fade" id = "update-doctor-profile-modal" tabindex = "-1" v-bind="$attrs">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5">Update Profile</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                            </div>

                                            <form @submit.prevent = "updateDoctorProfile">
                                                <!-- {{ doctor }} -->
                                                <div class="modal-body">
                                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                                        <input type = "text" class = "form-control" v-model = "doctor.doctor_user.user_name"
                                                        id="floatingInput">
                                                        <label for = "user_name" class = "form-label">Username</label>
                                                    </div>  

                                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                                        <input type = "text" class = "form-control" v-model = "doctor.doctor_user.password" placeholder = "Enter new password"
                                                        id="floatingInput">
                                                        <label for = "password" class = "form-label">Password</label>
                                                    </div> 

                                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                                        <input type = "text" class = "form-control" v-model = "doctor.name"
                                                        id="floatingInput">
                                                        <label for = "name" class = "form-label">Name</label>
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

                                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                                        <input type = "text" class = "form-control" v-model = "doctor.description"
                                                        id="floatingInput">
                                                        <label for = "description" class = "form-label">Description</label>
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

                                <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#view-profile" v-on:click="collapseProfile = !collapseProfile">
                                    <span v-if="collapseProfile">View Profile</span>
                                    <span v-else>Collapse Profile</span>
                                </button>
                            </div>
                        </div>
                        
                        <p><strong>Appointments Today:</strong> {{ doctor.today_appointment.length }}</p>
                        <p><strong>Appointments This Week:</strong> {{ doctor.upcoming_appointment.length }}</p>
                        <p><strong>Patients: </strong>{{ doctor.number_of_patients }}</p>
                        
                        <!-- collapse content -->
                        <div class = 'collapse' id = 'view-profile'>
                            <p><strong>Gender: </strong>{{ doctor.gender }}</p>
                            <p><strong>DOB: </strong>{{ doctor.dob }}</p>
                            <p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p>
                            <p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p>
                            <p><strong>Description: </strong>{{ doctor.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>                        
        
        <!-- other information  -->
        <div class = "m-4">
            <h4 class = "mb-4">Today's appointments ({{ doctor.today_appointment.length }})</h4>
            <div v-if = "doctor.today_appointment.length == 0">
                <p>No appointments scheduled today</p>
            </div>

            <div class = "d-flex justify-content-start flex-wrap gap-2">
                <div v-for="a in doctor.today_appointment">
                    <div class="card" style="min-height: 220px; max-width: 222px;">
                        <div class="card-body">
                            <h5 class="card-title">{{ a.app_patient.name }}</h5>
                            <div class = "border-top">
                                <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                <div v-if="a.status == 'Booked'">
                                    <button class = "btn btn-outline-secondary">Provide Details</button>
                                    <div class = "d-flex gap-2 mt-2">
                                        <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">Cancel</button>
                                        <button class = "btn btn-outline-primary">Reschedule</button>
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
    import { useUserStore } from '@/stores/userStore';

    import DoctorProfileUpdateModal from './DoctorProfileUpdateModal.vue';

    export default {
        name: "DoctorProfile",
        data() {
            return {
                store: useUserStore(),
                doctor: null,
                errorMessage: "",
                collapseProfile: true,
                user_name: null,
                password: null,
                name: null,
                dob: null,
                contact_number: null,
                email: null, 
                description: null
            }
        },
        components: {
            DoctorProfileUpdateModal
        },
        methods: {
            async getDoctor() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const display_doctor = await requestAPI('GET', null, `/doctor/${doctorID}?past_appointment=true&upcoming_appointment=true&availability=true&today_appointment=true`)
                    this.doctor = display_doctor
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            },
            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getDoctor()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async updateDoctorProfile() {
                try{
                    console.log("I am working")
                    const doctorID = this.store.user.doctor_id;
                    const data = {
                        user_name: this.doctor.doctor_user.user_name,
                        password: this.doctor.doctor_user.password,
                        name: this.doctor.name,
                        dob: this.doctor.dob,
                        contact_number: this.doctor.doctor_user.contact_number,
                        email: this.doctor.doctor_user.email,
                        description: this.doctor.description
                    }
                    const update_doctor = await requestAPI('PATCH', data, `/doctor/${doctorID}`)
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>