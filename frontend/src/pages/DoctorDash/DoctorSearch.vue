<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Contact Number ({{ lengthCN }})</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Email ({{ lengthEmail }})</button>
                    <button class="nav-link" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">Name ({{ lengthName }})</button>

                </div>                
            </div>

            <div class = "w-100 d-flex justify-content-end">
                <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>Go Back</button>
            </div>

            <div class = 'col w-75 mx-auto'>
                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                     <!-- Contact Number -->
                    <div class="tab-pane fade show active w-100" id="v-tab-profile" role="tabpanel">
                        <h4 class = "px-3">Patients</h4>
                            <ul class = "p-0">
                                <div v-if="patients">
                                    <div v-if="patients.contact_number.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="patient in patients.contact_number" class = "d-flex flex-column m-3">
                                        <!-- card for each patient  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${patient.pfp}.png`" height="100px">
                                                </div>
    
                                                <div>
                                                    <p><strong>{{patient.name}}</strong></p>
                                                </div>
                                            </div>
    
                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Gender: </strong>{{ patient.gender }}</p></div>
                                                    <div><p><strong>Age: </strong>{{ patient.get_age }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ patient.patient_user.email }}</p></div>
                                                    <div><p><strong>Appointments with you: </strong>{{ patient.number_of_appointments }}</p></div>
                                                    <div v-if="patient.last_visit == {}">
                                                        <p><strong>Last Visit: </strong></p>
                                                    </div>
                                                    <div v-else>
                                                        <p><strong>Last Visit: </strong>{{ patient.last_visit.date }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>

                        <h4 class = "px-3">Doctors</h4>
                            <ul class = "p-0">
                                <div v-if="doctors">
                                    <div v-if="doctors.contact_number.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="doctor in doctors.contact_number" class = "d-flex flex-column m-3">
                                        <!-- card for each doctor  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{doctor.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Department: </strong>{{ doctor.dept.name }}</p></div>
                                                    <div><p><strong>Gender: </strong>{{ doctor.gender }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                    </div>

                    <!-- Email  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <h4 class = "px-3">Patients</h4>
                            <ul class = "p-0">
                                <div v-if="patients">
                                    <div v-if="patients.email.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="patient in patients.email" class = "d-flex flex-column m-3">
                                        <!-- card for each patient  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${patient.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{patient.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Gender: </strong>{{ patient.gender }}</p></div>
                                                    <div><p><strong>Age: </strong>{{ patient.get_age }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ patient.patient_user.email }}</p></div>
                                                    <div><p><strong>Appointments with you: </strong>{{ patient.number_of_appointments }}</p></div>
                                                    <div v-if="patient.last_visit == {}">
                                                        <p><strong>Last Visit: </strong></p>
                                                    </div>
                                                    <div v-else>
                                                        <p><strong>Last Visit: </strong>{{ patient.last_visit.date }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>

                        <h4 class = "px-3">Doctors</h4>
                            <ul class = "p-0">
                                <div v-if="doctors">
                                    <div v-if="doctors.email.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="doctor in doctors.email" class = "d-flex flex-column m-3">
                                        <!-- card for each doctor  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{doctor.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Department: </strong>{{ doctor.dept.name }}</p></div>
                                                    <div><p><strong>Gender: </strong>{{ doctor.gender }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                    </div>

                    <!-- Name  -->
                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        <h4 class = "px-3">Patients</h4>
                            <ul class = "p-0">
                                <div v-if="patients">
                                    <div v-if="patients.name.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="patient in patients.name" class = "d-flex flex-column m-3">
                                        <!-- card for each patient  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${patient.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{patient.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Gender: </strong>{{ patient.gender }}</p></div>
                                                    <div><p><strong>Age: </strong>{{ patient.get_age }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ patient.patient_user.email }}</p></div>
                                                    <div><p><strong>Appointments with you: </strong>{{ patient.number_of_appointments }}</p></div>
                                                    <div v-if="patient.last_visit == {}">
                                                        <p><strong>Last Visit: </strong>--</p>
                                                    </div>
                                                    <div v-else>
                                                        <p><strong>Last Visit: </strong>{{ patient.last_visit.date }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                        <h4 class = "px-3">Doctors</h4>
                            <ul class = "p-0">
                                <div v-if="doctors">
                                    <div v-if="doctors.name.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <div v-else v-for="doctor in doctors.name" class = "d-flex flex-column m-3">
                                        <!-- card for each doctor  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{doctor.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Department: </strong>{{ doctor.dept.name }}</p></div>
                                                    <div><p><strong>Gender: </strong>{{ doctor.gender }}</p></div>
                                                    <div><p><strong>Contact Number: </strong>{{ doctor.doctor_user.contact_number }}</p></div>
                                                    <div><p><strong>Email: </strong>{{ doctor.doctor_user.email }}</p></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                        <h4 class = "px-3">Departments</h4>
                            <ul class = "p-0">
                                <div v-if="departments">
                                    <div v-if="departments.name.length == 0" class = "d-flex align-items-center justify-content-center" style="height: 200px;">
                                        <p>Nothing to show</p>
                                    </div>

                                    <!-- <li v-if="departments" v-for="department in departments.name">
                                        {{ department }}
                                    </li> -->

                                    <div v-else v-for="dept in departments.name" class = "d-flex flex-column m-3">
                                        <!-- card for each department  -->
                                        <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                                            <!-- photo container  -->
                                            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                                                <div class = "mt-2">
                                                    <img :src="`/images/${dept.pfp}.png`" height="100px">
                                                </div>

                                                <div>
                                                    <p><strong>{{dept.name}}</strong></p>
                                                </div>
                                            </div>

                                            <!-- information container -->
                                            <div class = "col-9 d-flex align-items-center">
                                                <div class = "d-flex flex-column m-2">
                                                    <div><p><strong>Description: </strong>{{ dept.description }}</p></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </ul>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    export default {
        name: "DoctorSearchPage",
        data() {
            return {
                result: null,
                lengthName: 0,
                lengthCN: 0,
                lengthEmail: 0,
                patients: null,
                doctors: null,
                departments: null
            }
        },

        methods: {
            async getSearchResults(query) { 
                const search_results = await requestAPI('GET', null, `/doctor/search?query=${query}`)
                this.result = search_results
                console.log(search_results)

                // assign for easier access
                this.patients = search_results.patients
                this.doctors = search_results.doctors
                this.departments = search_results.departments

                // length 
                this.lengthName = this.patients.name.length + this.doctors.name.length + this.departments.name.length
                this.lengthCN = this.patients.contact_number.length + this.doctors.contact_number.length
                this.lengthEmail = this.patients.email.length + this.doctors.email.length
            }
        },

        created() {
            this.getSearchResults(this.$route.params.query)
        },

        watch: {
            $route(new_route, old_route) {
                if (new_route.name == "doctorSearch") {
                    this.getSearchResults(this.$route.params.query)
                }
            }
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

    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>
