<template>
    <div class="container d-flex flex-column align-items-start flex-grow-1 min-vh-100">
        <div v-if="departments">
            <h4 class = "ms-5">Doctors</h4>
        </div>
        
        <div v-if="departments" class="col w-100">
            <div class = "d-flex justify-content-between w-75 mx-auto">
                <div class = "" v-for="dept in departments">
                    <button :class = "{'btn btn-outline-primary': true, 'active': selectedDept == dept.department_id}" @click="selectedDept = dept.department_id">{{ dept.name }}</button>
                </div>
            </div>
            <div v-for="dept in departments" class = "d-flex flex-column">
                 <div v-if="selectedDept == dept.department_id" class = "">
                    <div v-if="dept.doctors.length == 0" class = "w-100 mt-2 d-flex justify-content-center align-items-center" style="height: 50vh;">
                        <p>No doctors to show</p>
                    </div>
                    <div v-else v-for="doctor in dept.doctors" class = "px-5 m-3">
                        
                        <!-- card for each doctor  -->
                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow m-2" v-if="selectedDept == doctor.dept.department_id">
                            <!-- photo container  -->
                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                <div class = "mt-2">
                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                </div>
        
                                <div>
                                    <p><strong>Dr. {{ doctor.name }}</strong></p>
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
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: 'PatientDashDoctors',
        data() {
            return {
                departments: null,
                store: useUserStore(),
                selectedDept: 1
            }
        },
        methods: {
            async getDepartments() {
                try {
                    const display_departments = await requestAPI("GET", null, `/depts`)
                    this.departments = display_departments
                }
                catch(error) {
                    this.$emit(error.message)                   
                }
            }
        },
        mounted() {
            this.getDepartments()
        }
    }
</script>

<style scoped>
    .hover-shadow {
        transition: all 0.2s ease;
    }

    .hover-shadow:hover {
        transform: translateY(-5px);
        box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175)!important;
    }    
</style>