<template>
    <div class = "container" v-bind="$attrs">
        <div class = "d-flex justify-content-between w-75 mx-auto mb-3">
            <h2 class = "">Doctors</h2>

            <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addDoctorModal">
                Add Doctor
            </button>

            <!-- modal  -->
             <AddDoctorModal @form-add-doctor = "AddDoctor"/>
        </div>

        <div v-if="departments" class="col w-75 mx-auto">
            <div class = "d-flex justify-content-evenly flex-wrap">
                <div class="d-flex flex-grow-1" v-for="dept in departments">
                    <a :class = "{'dept-buttons w-100 text-center pb-2': true, 'dept-buttons-active': selectedDept == dept.department_id}" @click="selectedDept = dept.department_id">{{ dept.name }}</a>
                </div>
            </div>

            <div v-for="dept in departments" class = "d-flex flex-column w-100">
                <div v-if="selectedDept == dept.department_id">
                    <div v-if="dept.doctors.length == 0" class = "w-100 mt-2 d-flex justify-content-center align-items-center" style="height: 50vh;">
                        <p>No doctors to show</p>
                    </div>
                    
                    <div v-else v-for="doctor in dept.doctors">

                        <!-- card for each doctor  -->
                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow mb-2 mt-2" v-if="selectedDept == doctor.dept.department_id">
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
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import { requestAPI } from '../../../utils/api';
    
    import AddDoctorModal from './AddDoctorModal.vue';

    export default {
        name: 'AdminDashDoctor',
        emits: ['error', 'success'],
        data() {
            return {
                departments: [],
                selectedDept: 1
            }
        },
        components: {
            AddDoctorModal
        },
        methods: {
            async PopulateDoctor() {
                try {
                    const display_departments = await requestAPI("GET", null, `/depts`)
                    this.departments = display_departments
                }
                catch(error) {
                    this.$emit('error', error.message)                  
                }
            },
            async AddDoctor(data) {
                try {
                    const add_doctor = await requestAPI("POST", data, "/doctor")
                    this.PopulateDoctor()
                    this.$emit('success', 'Doctor added successfully!')
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        },

        mounted() {
            this.PopulateDoctor()
        }
    }
</script>

<style scoped>
    .dept-buttons {
        border-radius: 0;
        text-decoration: none;
        cursor: pointer;
        color: black;
    }
    .dept-buttons-active {
        text-decoration: none;
        border-bottom: 2px solid orangered !important;
        cursor: pointer !important;
    }

    .hover-shadow {
        transition: all 0.2s ease;
    }

    .hover-shadow:hover {
        transform: translateY(-5px);
        box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175)!important;
    } 
</style>