<template>
    <div class = "container" v-bind="$attrs">
        <div class = "d-flex justify-content-between">
            <h2>Doctors</h2>

            <button class = 'btn btn-primary' type="button" data-bs-toggle="collapse" data-bs-target="#add-doc-button">
                Add
            </button>
        </div>
    </div>

    <div class = 'collapse' id = 'add-doc-button'>
        <div class = 'card card-body'>
            <form>
                <div class = 'row'>
                    <div class = 'row'>
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_user_name floatingInput">
                            <label for="doc_user_name" class="form-label">User Name*</label>
                        </div> 
                                        
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_password floatingInput">
                            <label for="doc_password" class="form-label">Password*</label>
                        </div>  

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_name floatingInput">
                            <label for="doc_name" class="form-label">Name*</label>
                        </div>               
                    </div>

                    <div class = 'row'>
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_contact_number floatingInput">
                            <label for="doc_contact_number" class="form-label">Contact Number</label>
                        </div>   

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_email floatingInput">
                            <label for="doc_email" class="form-label">Email</label>
                        </div>   

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="date" class="form-control"
                            id="doc_dob floatingInput">
                            <label for="doc_dob" class="form-label">DOB</label>
                        </div>                                        
                    </div>

                    <div class = 'row'>
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <select class="form-select">
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <label for="gender" class="form-label">Gender</label>  
                        </div>    

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control"
                            id="doc_desc floatingInput">
                            <label for="doc_desc" class="form-label">Description</label>
                        </div>    
                    </div>
                    <div class = 'row d-flex flex-column align-items-center'><button type="submit" class="btn btn-primary col-2">Submit</button></div>
                </div>             
            </form>
        </div>
    </div>

    <table class = 'table table-striped table-hover'>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Contact Number</th>
                <th>Email</th>
                <th>Info</th>
            </tr>
        </thead>

        <tbody>
            <template v-for="(doctor, index) in doctors" :key="doctor.doctor_id">
                <tr>
                    <td><RouterLink :to = "`/admin/doctor/${doctor.doctor_id}`">{{ doctor.doctor_id }}</RouterLink></td>
                    <td>{{ doctor.name }}</td>
                    <td>{{ doctor.doctor_user.contact_number }}</td>
                    <td>{{ doctor.doctor_user.email }}</td>
                    <td @click="expandRow(index)">Click for more info</td>
                </tr>

                <tr v-show="additionalData[index]">
                    <td colspan="6">
                        <div class="row">
                            <div>
                                <img src = '../../assets/DefaultDepartment.png' height="200px" width="200px">
                            </div>

                            <div class = 'row'>
                                <p>{{ doctor.description }}</p>
                            </div>
                        </div>
                    </td>
                </tr>
            </template>
        </tbody>
    </table>  
</template>


<script setup>
    import { ref, reactive } from 'vue'

    const additionalData = ref({})

    const expandRow = (index) => {
        additionalData.value[index] = !additionalData.value[index]
    }

    
</script>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashDoctor',
        emits: ['error'],
        data() {
            return {
                doctors: [],
            }

        },

        methods: {
            async PopulateDoctor() {
                try {
                    const all_doctors = await requestAPI('GET', null, '/doctors')
                    this.doctors = all_doctors
                }
                catch(error) {
                    this.$emit('error', error.message) 
                }
            },
        },

        mounted() {
            this.PopulateDoctor()
        }
    }
</script>