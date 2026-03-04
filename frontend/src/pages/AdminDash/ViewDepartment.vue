<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Doctors</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Upcoming Appointments</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Past Appointments</button>
                </div>                
            </div>

            <div v-if="department" class = 'col'>
                
                <!-- Always visible -->
                <div class = 'container'>
                    <div class = "d-flex justify-content-between">
                        <h2>Department of {{ department.name }}</h2>

                        <div class = "d-flex gap-1">
                            <button class = "btn btn-primary" type = "button" data-bs-toggle="modal" data-bs-target="#exampleModal">Update</button>
                            <button class = "btn btn-primary" v-on:click="deleteDepartment">Delete</button>
                        </div>
                    </div>

                    <div class = 'row'>
                        <div class = 'col-sm-3'><img :src="`/images/${department.pfp}.png`" height="200px"></div>
                        <div class = 'col'>{{ department.description }}</div>
                    </div>
                </div>

                <!-- Modal -->
                <div class="modal fade" id="exampleModal" tabindex="-1">
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
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                    <button type="submit" class="btn btn-primary">Save changes</button>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Doctors  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <ul>
                            <li v-for="doctor in department.doctors">
                                <h3>{{ doctor.name }}</h3>
                                <p>{{ doctor.description }}</p>
                            </li>
                        </ul>
                    </div>

                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <div v-if = "ua">
                            <ol>
                                <li v-for = "a in department.upcoming_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Doctor:</strong> {{ a.app_doctor.name }}</p>
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
                                <li v-for = "a in department.past_appointment">
                                    <p><strong>Appointment ID:</strong> {{ a.appointment_id }}</p>
                                    <p><strong>Doctor:</strong> {{ a.app_doctor.name }}</p>
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
        name: 'ViewDepartment',
        data() {
            return {
                department: null, 
                ua: false,
                pa: false,
                name: null,
                description: null            
            }
        },
        methods: {
            async getDepartment() {
                const deptId = this.$route.params.deptId;
                const display_dept = await requestAPI('GET', null, `/dept/${deptId}?past_appointment=true&upcoming_appointment=true`)
                this.department = display_dept
                
                // check if there are any upcoming appointments
                if (this.department.upcoming_appointment.length != 0) {
                    this.ua = true
                }

                // check if there are any past appointments
                if (this.department.past_appointment.length != 0) {
                    this.pa = true
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
                }
                catch(error) {
                    console.error('Error updating department:', error)
                }
            },

            async deleteDepartment() {
                try {
                    const deptId = this.$route.params.deptId;
                    const delete_department = await requestAPI('DELETE', null, `/dept/${deptId}`)
                    this.$router.push("/admin")
                }
                catch(error) {
                    console.error('Error deleting department:', error)
                }
            }
        },
        mounted() {
            this.getDepartment()
        }
    }
</script>