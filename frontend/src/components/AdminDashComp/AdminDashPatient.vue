<template>
    <div class = "container" v-bind="$attrs">
        <div class = "d-flex justify-content-between w-75 mx-auto mb-3">
            <h2>Patients</h2>

            <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addPatientModal">
                Add Patient
            </button>

            <!-- modal  -->
            <AddPatientModal @form-add-patient = "AddPatient"/>
        </div>
    </div>

    <div class = "w-75 mx-auto d-flex gap-2 flex-column">
        <!-- card for each patient  -->
        <div v-for = 'patient in patients' class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow">
            <!-- photo container  -->
            <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                <div class = "mt-2">
                    <img :src="`/images/${patient.pfp}.png`" height="100px">
                </div>

                <div>
                    <p><strong><RouterLink :to = "`/admin/patient/${patient.patient_id}`">{{ patient.name }}</RouterLink></strong></p>
                </div>
            </div>

            <!-- information container -->
            <div class = "col-9 d-flex align-items-center">
                <div class = "d-flex flex-column m-2">
                    <div><p><strong>ID: </strong>{{ patient.patient_id }}</p></div>
                    <div><p><strong>Gender: </strong>{{ patient.gender }}</p></div>
                    <div><p><strong>Age: </strong>{{ patient.get_age }}</p></div>
                    <div><p><strong>Contact Number: </strong>{{ patient.patient_user.contact_number }}</p></div>
                    <div><p><strong>Email: </strong>{{ patient.patient_user.email }}</p></div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import { requestAPI } from '../../../utils/api';

    import AddPatientModal from './AddPatientModal.vue';

    export default {
        name: 'AdminDashPatient',
        emits: ['error', 'success'],
        data() {
            return {
                patients: [],
                showTable: true
            }
        },
        components: {
            AddPatientModal
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
            },
            async AddPatient(data) {
                try {
                    const add_doctor = await requestAPI("POST", data, "/register")
                    this.PopulatePatients()
                    this.$emit('success', 'Patient added successfully!')
                }
                catch(error) {
                    this.$emit('error', error.message || 'An error occurred')
                }
            }
        },
        mounted() {
            this.PopulatePatients()
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
</style>