<template>
    <div class="modal fade" id="addDoctorModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Doctor</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form @submit.prevent = "SubmitAddDoctorForm">
                    <div class="modal-body">
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "user_name"
                            id="doc_user_name floatingInput">
                            <label for="doc_user_name" class="form-label">User Name*</label>
                        </div> 
                                        
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "user_password"
                            id="doc_password floatingInput">
                            <label for="doc_password" class="form-label">Password*</label>
                        </div>  

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "name"
                            id="doc_name floatingInput">
                            <label for="doc_name" class="form-label">Name*</label>
                        </div> 
                                     
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <select v-model="department" class="form-select">
                                <option disabled value="0">Please select a department</option>
                                <option v-for="dept in departments" :key="dept.department_id" 
                                        :value="dept.department_id">
                                    {{ dept.name }}
                                </option>
                            </select>
                            <label for="gender" class="form-label">Department</label> 
                        </div>               

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "contact_number"
                            id="doc_contact_number floatingInput">
                            <label for="doc_contact_number" class="form-label">Contact Number</label>
                        </div>   

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "email"
                            id="doc_email floatingInput">
                            <label for="doc_email" class="form-label">Email*</label>
                        </div>   

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="date" class="form-control" v-model = "dob"
                            id="doc_dob floatingInput">
                            <label for="doc_dob" class="form-label">DOB</label>
                        </div>                                        

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <select v-model="gender" class="form-select">
                                <option disabled value="">Please select gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <label for="gender" class="form-label">Gender</label>  
                        </div>    

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "description"
                            id="doc_desc floatingInput">
                            <label for="doc_desc" class="form-label">Description</label>
                        </div>    
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-outline-primary">Add Doctor</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    export default {
        name: 'AddDoctorModal',
        data() {
            return {
                user_name: '',
                user_password: '',
                name: '',
                contact_number: '',
                email: '',
                dob: null,
                gender: '',
                description: '',
                department: 0,
                departments: []
            }
        },
        emits: ["error", "form-add-doctor"],
        methods: {
            async SubmitAddDoctorForm() {
                try {
                    const data = {
                        user_name: this.user_name,
                        user_password: this.user_password,
                        name: this.name,
                        gender: this.gender,
                        dob: this.dob,
                        email: this.email,
                        contact_number: this.contact_number,
                        description: this.description,
                        department: this.department
                    }
                    this.$emit("form-add-doctor", data)
                    bootstrap.Modal.getInstance(document.getElementById("addDoctorModal")).hide()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            },
            async getDepartments() {
                try {
                    const all_departments = await requestAPI("GET", null, "/depts")
                    this.departments = all_departments
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            }
        },
        mounted() {
            this.getDepartments()
        }
    }
</script>