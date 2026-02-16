<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">ID ({{ lengthID }})</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Contact Number ({{ lengthCN }})</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Email ({{ lengthEmail }})</button>
                    <button class="nav-link" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">Name ({{ lengthName }})</button>

                </div>                
            </div>

            <div class = 'col'>
                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- ID  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <h4>Patients</h4>
                            <ul>
                                <li v-if="patients" v-for="patient in patients.ID">
                                    {{ patient }}
                                </li>
                            </ul>
                        <h4>Doctors</h4>
                            <ul>
                                <li v-if="doctors" v-for="doctor in doctors.ID">
                                    {{ doctor }}
                                </li>
                            </ul>
                        <h4>Departments</h4>
                            <ul>
                                <li v-if="departments" v-for="department in departments.ID">
                                    {{ department }}
                                </li>
                            </ul>
                    </div>

                    <!-- Contact Number -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <h4>Patients</h4>
                            <ul>
                                <li v-if="patients" v-for="patient in patients.contact_number">
                                    {{ patient }}
                                </li>
                            </ul>
                        <h4>Doctors</h4>
                            <ul>
                                <li v-if="doctors" v-for="doctor in doctors.contact_number">
                                    {{ doctor }}
                                </li>
                            </ul>
                    </div>

                    <!-- Email  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <h4>Patients</h4>
                            <ul>
                                <li v-if="patients" v-for="patient in patients.email">
                                    {{ patient }}
                                </li>
                            </ul>
                        <h4>Doctors</h4>
                            <ul>
                                <li v-if="doctors" v-for="doctor in doctors.email">
                                    {{ doctor }}
                                </li>
                            </ul>
                    </div>

                    <!-- Name  -->
                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        <h4>Patients</h4>
                            <ul>
                                <li v-if="patients" v-for="patient in patients.name">
                                    {{ patient }}
                                </li>
                            </ul>
                        <h4>Doctors</h4>
                            <ul>
                                <li v-if="doctors" v-for="doctor in doctors.name">
                                    {{ doctor }}
                                </li>
                            </ul>
                        <h4>Departments</h4>
                            <ul>
                                <li v-if="departments" v-for="department in departments.name">
                                    {{ department }}
                                </li>
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
        name: "AdminSearchPage",
        data() {
            return {
                result: null,
                lengthID: 0,
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
                const search_results = await requestAPI('GET', null, `/admin/search?query=${query}`)
                this.result = search_results

                // assign for easier access
                this.patients = search_results.patients
                this.doctors = search_results.doctors
                this.departments = search_results.departments

                // length 
                this.lengthID = this.patients.ID.length + this.doctors.ID.length + this.departments.ID.length
                this.lengthName = this.patients.name.length + this.doctors.name.length + this.departments.name.length
                this.lengthCN = this.patients.contact_number.length + this.doctors.contact_number.length
                this.lengthEmail = this.patients.email.length + this.doctors.email.length
            }
        },

        created() {
            this.getSearchResults(this.$route.params.query)
        }
    }
</script>