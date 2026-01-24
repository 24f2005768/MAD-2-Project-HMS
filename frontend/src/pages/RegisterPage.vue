<template>
    <div class="container d-flex flex-column align-items-center flex-grow-1">
        <h1>This is homepage</h1>
        <form @submit.prevent = "RegisterPatient">
        <div class = 'row'>
            <div class="row">
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

            <div class="row">
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

            <div class="row">
                <div class="col-md row-sm mb-3 form-floating">
                    <select class="form-select" aria-label="Default select example" v-model="gender">
                        <option selected>Select your gender</option>
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
        <div class = 'row d-flex flex-column align-items-center'><button type="submit" class="btn btn-primary col-2">Submit</button></div>
        </div>
    </form>
    </div>
</template>

<script>
    import { useUserStore } from '@/stores/userStore';
    import { requestAPI } from '../../utils/api';

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
                weight: null
            }
        },

        methods: {
            async RegisterPatient() {
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
        }
    }
</script>