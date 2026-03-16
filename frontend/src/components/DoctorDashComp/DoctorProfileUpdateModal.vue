<template>
    <div class = "modal fade" id = "update-doctor-profile-modal" tabindex = "-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Update Profile</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form v-if="doctor && doctor.doctor_user" @submit.prevent = "submitForm">
                    <div class="modal-body">
                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "doctor.doctor_user.user_name"
                            id="floatingInput">
                            <label for = "user_name" class = "form-label">Username</label>
                        </div>  

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "password" 
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

</template>

<script>
    export default {
        name: 'DoctorProfileUpdateModal',
        props: {
            doctor: {
                type: Object,
                required: true
            }
        },
        emits: ["update-profile", "error"],
        data() {
            return {
                password: "",
            }
        },
        methods: {
            async submitForm() {
                try {
                    const data = {
                        user_name: this.doctor.doctor_user.user_name,
                        password: this.password,
                        name: this.doctor.name,
                        dob: this.doctor.dob,
                        contact_number: this.doctor.doctor_user.contact_number,
                        email: this.doctor.doctor_user.email,
                        description: this.doctor.description
                    }
                    this.$emit("update-profile", data)
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        }
    }
</script>