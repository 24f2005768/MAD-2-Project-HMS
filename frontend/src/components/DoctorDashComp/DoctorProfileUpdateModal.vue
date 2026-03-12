<template>
    <div v-if="doctor" class = "modal fade" id = "update-doctor-profile-modal" tabindex = "-1" v-bind="$attrs">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Update Profile</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form>
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
                        <button type="submit" class="btn btn-primary" v-on:click="updateDoctorProfile">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: 'DoctorProfileUpdateModal',
        data() {
            return {
                store: useUserStore(), 
                doctor: null,
                user_name: null,
                password: null,
                name: null,
                dob: null,
                contact_number: null,
                email: null, 
                description: null
            }
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
            async updateDoctorProfile() {
                try{
                    console.log("I am working")
                    const doctorID = this.store.user.doctor_id;
                    const data = {
                        user_name: this.doctor.doctor_user.user_name,
                        password: this.doctor.doctor_user.password,
                        name: this.doctor.name,
                        dob: this.doctor.dob,
                        contact_number: this.doctor_user.doctor.name,
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