<template>
    <div class="modal fade" id="addPatientModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Patient</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form @submit.prevent = "SubmitAddPatientForm">
                    <div class="modal-body">
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model = "user_name"
                            id="user_name floatingInput">
                            <label for="user_name" class="form-label">User Name*</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="password" class="form-control" v-model = "user_password"
                            id="user_password">
                            <label for="user_password" class="form-label">Password*</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="email" class="form-control" v-model="email"
                            id="email">
                            <label for="email" class="form-label">Email*</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="tel" class="form-control" v-model = "contact_number"
                            id="contact_number">
                            <label for="contact_number" class="form-label">Contact Number</label>
                        </div>


                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="text" class="form-control" v-model = "name"
                            id="name">
                            <label for="name" class="form-label">Name*</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="date" class="form-control" v-model="dob"
                            id="dob">
                            <label for="dob" class="form-label">DOB</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <select class="form-select" v-model = "gender">
                                <option disabled value="">Please select gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <label for="gender" class="form-label">Gender</label>              
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" min="0" v-model = "height"
                            id="height">
                            <label for="height" class="form-label">Height in cm</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" min="0" v-model = "weight"
                            id="weight"> 
                            <label for="weight" class="form-label">Weight in kg</label>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-outline-primary">Add Patient</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    export default {
        name: 'AddPatientModal',
        data() {
            return {
                user_name: '',
                user_password: '',
                email: '',
                contact_number: '',
                name: '',
                dob: null,
                gender: '',
                height: null,
                weight: null,
            }
        },
        emits: ["error", "form-add-patient"],
        methods: {
            async SubmitAddPatientForm() {
                try {
                    const data = {
                        user_name: this.user_name,
                        user_password: this.user_password,
                        email: this.email,
                        contact_number: this.contact_number,
                        name: this.name,
                        dob: this.dob,
                        gender: this.gender,
                        height: this.height,
                        weight: this.weight
                    }
                    this.$emit("form-add-patient", data)
                    bootstrap.Modal.getInstance(document.getElementById('addPatientModal')).hide()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            }
        }
    }
</script>