<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Doctors
                    </button>

                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">
                        Upcoming Appointments
                    </button>

                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">
                        Past Appointments
                    </button>
                </div>                
            </div>

            <div v-if="department" class = 'col'>
                
                <!-- Always visible -->
                <div class="d-flex justify-content-end">
                    <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>
                        Go Back
                    </button>
                </div>
                
                <div class = 'card container my-2'>
                    <div class = "d-flex justify-content-between my-3">
                        <h2>Department of {{ department.name }}</h2>                            
                        <div class="d-flex justify-content-end gap-2">
                            <button class = "btn btn-outline-secondary" type = "button" data-bs-toggle="modal" data-bs-target="#update-dept-modal">
                                Update
                            </button>
        
                            <button class = "btn btn-outline-danger" v-on:click="deleteDepartment">
                                Delete
                            </button>
                        </div>
                    </div>

                    <div class = 'row'>
                        <div class = 'col-sm-3'><img :src="`/images/${department.pfp}.png`" height="200px"></div>
                        <div class = 'col d-flex'>
                            <p><strong>Description:</strong> {{ department.description }}</p>
                        </div>
                    </div>
                </div>

                <!-- Modal -->
                <div class="modal fade" id="update-dept-modal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Update Department Details</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <form @submit.prevent = "updateDepartment">
                                <div class="modal-body">
                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "department.name"
                                        id="floatingInput">
                                        <label for = "name" class = "form-label">Name</label>
                                    </div>

                                    <div class = "col-md row-sm mb-3 form-floating form-floating">
                                        <input type = "text" class = "form-control" v-model = "department.description"
                                        id="floatingInput">
                                        <label for = "name" class = "form-label">Description</label>
                                    </div>
                                </div>
                                
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-outline-primary">Update Department</button>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Doctors  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <h3 class = "px-2 mt-3">Our Doctors ({{ department.doctors.length }})</h3>
                        
                        <!-- card for each doctor  -->
                        <div class = "d-flex flex-row w-100 h-auto border-bottom mb-2 mt-2" v-for="doctor in department.doctors">
                            <!-- photo container  -->
                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                <div class = "mt-2">
                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                </div>
        
                                <div>
                                    <p>
                                        <strong>
                                            <RouterLink :to = "`/admin/doctor/${doctor.doctor_id}`" style="color: black;">
                                                Dr. {{ doctor.name }}
                                            </RouterLink>
                                        </strong>
                                    </p>
                                </div>
                            </div>
        
                            <!-- information container -->
                            <div class = "col-9 d-flex align-items-center">
                                <div class = "d-flex flex-column m-2">
                                    <div><p><strong>Gender: </strong>{{ doctor.gender }}</p></div>
                                    <div><p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p></div>
                                    <div><p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p></div>
                                    <div><p><strong>Description: </strong>{{ doctor.description }}</p></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade w-100 mt-3" id="v-tab-profile" role="tabpanel">
                        <h3 class = "mb-3">Upcoming Appointments ({{ department.upcoming_appointment.length }})</h3>
                        <div v-if = "department.upcoming_appointment.length == 0">
                            <p>No upcoming appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in department.upcoming_appointment">
                                <div class="card" style="height: 270px; width: 235px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Doctor: </strong>Dr. {{ a.app_doctor.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Patient: </strong>{{ a.app_patient.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>

                                            <div v-if="a.status == 'Booked'">
                                                <div class = "d-flex gap-2 mt-2">
                                                    <button class = "btn btn-outline-danger" v-on:click="cancelAppointment(a.appointment_id)">
                                                        Cancel
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100 mt-3" id="v-tab-messages" role="tabpanel">
                        <h3 class = "mb-3">Past Appointments ({{ department.past_appointment.length }})</h3>
                        <div v-if = "department.upcoming_appointment.length == 0">
                            <p>No past appointments</p>
                        </div>

                        <div class = "d-flex justify-content-start flex-wrap  gap-2">
                            <div v-for="a in department.upcoming_appointment">
                                <div class="card" style="height: 270px; width: 235px;">
                                    <div class="card-body">
                                        <h5 class="card-text mb-2"><strong>Date: </strong>{{ a.date }}</h5>  
                                        <div class = "border-top">
                                            <p class="card-text mt-2 mb-2"><strong>Doctor: </strong>Dr. {{ a.app_doctor.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Patient: </strong>{{ a.app_patient.name }}</p>
                                            <p class="card-text mt-2 mb-2"><strong>Time: </strong>{{ a.start_time }} - {{ a.end_time }}</p>
                                            <p class="card-text mb-2"><strong>Status: </strong>{{ a.status }}</p>
                                            <div class = "d-flex gap-2 mt-2">
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
        name: 'ViewDepartment',
        data() {
            return {
                department: null,
                name: null,
                description: null            
            }
        },
        components: {
            errorToast,
            successToast
        },
        methods: {
            async getDepartment() {
                try {
                    const deptId = this.$route.params.deptId;
                    const display_dept = await requestAPI('GET', null, `/dept/${deptId}?past_appointment=true&upcoming_appointment=true`)
                    this.department = display_dept
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async updateDepartment() {
                try {
                    const deptId = this.$route.params.deptId;
                    const data = {
                        name: this.department.name,
                        description: this.department.description,
                    }

                    const update_dept = await requestAPI('PATCH', data, `/dept/${deptId}`)
                    this.successHandler("Department updated successfully")
                    bootstrap.Modal.getInstance(document.getElementById('update-dept-modal')).hide()
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async deleteDepartment() {
                try {
                    const deptId = this.$route.params.deptId;
                    const delete_department = await requestAPI('DELETE', null, `/dept/${deptId}`)
                    this.$router.push("/admin")
                }
                catch(error) {
                    this.errorHandler(error.message)
                }
            },

            async cancelAppointment(appointmentID) {
                try {
                    const cancel_appointment = await requestAPI("PATCH", null, `/cancel-appointment/${appointmentID}`)
                    this.getDepartment()
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