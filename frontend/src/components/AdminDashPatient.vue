<template>
    <div class = "container" v-bind="$attrs">
        <div class = "d-flex justify-content-between">
            <h2>Patients</h2>

            <button class = 'btn btn-primary' type="button" data-bs-toggle="collapse" data-bs-target="#add-dept-button">
                Add
            </button>
        </div>
    </div>
    <!-- Add patient  -->
    <div class = 'collapse' id = 'add-dept-button'>
        <div class = 'card card-body'>
            <form @submit.prevent = "RegisterPatient">
                <div class = 'row'>
                    <div class="row">
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" placeholder="User Name*"
                            id="user_name floatingInput">
                            <label for="user_name" class="form-label">User Name</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="password" class="form-control" placeholder="Password*"
                            id="user_password">
                            <label for="user_password" class="form-label">Password</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="email" class="form-control" placeholder="Email"
                            id="email">
                            <label for="email" class="form-label">Email</label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="tel" class="form-control" placeholder="Contact Number"
                            id="contact_number">
                            <label for="contact_number" class="form-label">Contact Number</label>
                        </div>


                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="text" class="form-control"  placeholder="Name*"
                            id="name">
                            <label for="name" class="form-label">Name</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="date" class="form-control"
                            id="dob">
                            <label for="dob" class="form-label">DOB</label>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md row-sm mb-3 form-floating">
                            <select class="form-select">
                                <option selected>Select your gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                            <label for="gender" class="form-label">Gender</label>              
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" placeholder="Height" min="0"
                            id="height">
                            <label for="height" class="form-label">Height in cm</label>
                        </div>

                        <div class="col-md row-sm mb-3 form-floating">
                            <input type="number" class="form-control" placeholder="Weight" min="0"
                            id="weight"> 
                            <label for="weight" class="form-label">Weight in kg</label>
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
                <th>DOB</th>
                <th>Contact Number</th>
                <th>Email</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for = 'patient in patients'>
                <td><RouterLink :to = "`/admin/patient/${patient.patient_id}`">{{ patient.patient_id }}</RouterLink></td>
                <td>{{ patient.name }}</td>
                <td>{{ patient.dob }}</td>
                <td>{{ patient.patient_user.contact_number }}</td>
                <td>{{ patient.patient_user.email }}</td>
                <td>Edit</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashPatient',
        emits: ['error'],
        data() {
            return {
                patients: [],
                showTable: true
            }
        },
        methods: {
            async PopulatePatients() {
                try {
                    const all_patients = await requestAPI('GET', null, '/patients')
                    this.patients = all_patients
                }
                catch(error) {
                    this.$emit('error', error.message) 
                }
            }
        },
        mounted() {
            this.PopulatePatients()
        }
    }
</script>