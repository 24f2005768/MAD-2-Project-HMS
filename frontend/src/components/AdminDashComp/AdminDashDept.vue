<template>
    <div class = 'container' v-bind="$attrs">
        <div class = 'd-flex justify-content-between w-75 mx-auto'>
            <div>
                <h2>Departments</h2>
            </div>
            
            <div>
                <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addDeptModal">
                    Add Department
                </button>

                <!-- modal  -->
                <AddDepartmentModal @form-add-department = "AddDepartment"/>
            </div>
        </div>
    </div>

    <div v-if="departments" class="col w-75 mx-auto">     
        <div v-for="dept in departments" class = "d-flex flex-column">
                <!-- <div v-if="dept.doctors.length == 0" class = "w-100 mt-2 d-flex justify-content-center align-items-center" style="height: 50vh;">
                    <p>No doctors to show</p>
                </div> -->
                    
            <!-- card for each department  -->
            <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow m-2">
                <!-- photo container  -->
                <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                    <div class = "mt-2">
                        <img :src="`/images/${dept.pfp}.png`" height="100px">
                    </div>

                    <div>
                        <p>
                            <strong>
                                <RouterLink :to = "`/admin/dept/${dept.department_id}`" style="color: black;">
                                    {{ dept.name }}
                                </RouterLink>
                            </strong>
                        </p>
                    </div>
                </div>

                <!-- information container -->
                <div class = "col-9 d-flex align-items-center">
                    <div class = "d-flex flex-column m-2">
                        <div><p><strong>Description: </strong>{{ dept.description }}</p></div>
                        <div><p><strong>Doctors: </strong>{{ dept.doctors.length }}</p></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    import AddDepartmentModal from './AddDepartmentModal.vue';

    export default {
        name: 'AdminDashDept',
        emits: ['error', 'success'],
        data() {
            return {
                departments: []
            }
        },
        components: {
            AddDepartmentModal
        },
        methods: {
            async PopulateDept() {
                try {
                    const all_departments = await requestAPI('GET', null, '/depts')
                    this.departments = all_departments
                }
                catch(error) {
                this.$emit('error', error.message) 
                }
            },
            async AddDepartment(data) {
                try {
                    const add_doctor = await requestAPI("POST", data, "/dept")
                    this.PopulateDept()
                    this.$emit('success', 'Department added successfully!')
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        },
        mounted() {
            this.PopulateDept()
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