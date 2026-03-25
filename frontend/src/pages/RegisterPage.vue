<template>
    <div class="container d-flex flex-column align-items-center justify-content-center flex-grow-1 min-vw-100 gap-3" style="min-height: 90vh;">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

        <div class = "w-100 d-flex justify-content-center">
            <h3 class>Register</h3>
        </div>

        <div class = 'card row d-flex flex-column justify-content-center align-items-center gap-2 w-50'>
            <form @submit.prevent = "RegisterPatient">
                
                <div class = 'row'>
                    <!-- user name, password, email  -->
                    <div class="row mt-3 mb-3">
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" placeholder="User Name*" v-model="user_name"
                            id="user_name floatingInput">
                            <label for="user_name" class="form-label">User Name</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="password" class="form-control" placeholder="Password*" v-model="user_password"
                            id="user_password">
                            <label for="user_password" class="form-label">Password</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="email" class="form-control" placeholder="Email" v-model="email"
                            id="email">
                            <label for="email" class="form-label">Email</label>
                        </div>
                    </div>

                    <div class="row mt-3 mb-3">
                        <!-- contact_number name dob  -->
                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="tel" class="form-control" placeholder="Contact Number" v-model="contact_number"
                            id="contact_number">
                            <label for="contact_number" class="form-label">Contact Number</label>
                        </div>


                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="text" class="form-control"  placeholder="Name*" v-model="name"
                            id="name">
                            <label for="name" class="form-label">Name</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="date" class="form-control" v-model="dob"
                            id="dob">
                            <label for="dob" class="form-label">DOB</label>
                        </div>
                    </div>

                    <div class="row mt-3 mb-3">
                        <!-- gender, weight, height  -->
                        <div class="col-md row-sm mb-3 form-floating">
                            <select class="form-select" aria-label="Default select example" v-model="gender">
                                <option disabled value="">Please select gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <label for="gender" class="form-label">Gender</label>              
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" placeholder="Height" min="0" v-model="height"
                            id="height">
                            <label for="height" class="form-label">Height in cm</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" placeholder="Weight" min="0" v-model="weight"
                            id="weight"> 
                            <label for="weight" class="form-label">Weight in kg</label>
                        </div>
                    </div>

                    <div class = 'row d-flex flex-column align-items-center mb-3'>
                        <button type="submit" class="btn btn-outline-primary col-2">
                            Submit
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    import { useUserStore } from '@/stores/userStore';
    import { requestAPI } from '../../utils/api';
    import errorToast from '@/components/errorToast.vue';

    export default {
        name: 'RegisterPage',
        data() {
            return {
                store: useUserStore(),
                user_name: '',
                user_password: '',
                email: '',
                contact_number: '',
                name: '',
                dob: null,
                gender: '',
                height: null,
                weight: null,
                errorMessage: ''
            }
        },
        components: {
            errorToast
        },
        methods: {
            async RegisterPatient() {
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
                    const res = await requestAPI('POST', data,'/register');
                    this.$router.push('/')
                }
                catch(error) {
                    this.errorHandler(error.message);
                }
            },
            errorHandler(message) {
                    this.errorMessage = message;
                    }
        }
    }
</script>