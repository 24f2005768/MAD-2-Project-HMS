<template>
    <div class="container d-flex flex-column align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div v-if="patients">
            <h4 class = "ms-5">Patients ({{ patientCount }})</h4>
        </div>

        <div v-if="patients" class="w-75">
            <div v-for="patientName in Object.keys(patients)" :key = 'patientName' class = "d-flex flex-column px-5 m-3">
               
                <!-- card for each patient  -->
                <div class = "card d-flex flex-row w-100 h-auto shadow-sm hover-shadow" >
                    <!-- photo container  -->
                    <div class = "col-3 d-flex flex-column justify-content-center align-items-center">
                        <div class = "mt-2">
                            <img :src="`/images/${patients[patientName].patient_data.pfp}.png`" height="100px">
                        </div>

                        <div>
                            <p><strong>{{patients[patientName].patient_data.name}}</strong></p>
                        </div>
                    </div>

                    <!-- information container -->
                    <div class = "col-9 d-flex align-items-center">
                        <div class = "d-flex flex-column m-2">
                            <div><p><strong>Gender: </strong>{{ patients[patientName].patient_data.gender }}</p></div>
                            <div><p><strong>Age: </strong>{{ patients[patientName].patient_data.get_age }}</p></div>
                            <div><p><strong>Appointments with you: </strong>{{ patients[patientName].patient_data.number_of_appointments }}</p></div>
                            <div><p><strong>Last Visit: </strong>{{ patients[patientName].patient_data.last_visit.date }}</p></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: 'DoctorDashPatients',
        data() {
            return {
                patients: null,
                patientCount: 0,
                store: useUserStore()
            }
        },
        methods: {
            async getPatients() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const display_patients = await requestAPI("GET", null, `/doctor/${doctorID}?patients=true`)
                    this.patientCount = display_patients.number_of_patients
                    this.patients = display_patients.patients
                }
                catch(error) {
                    console.error("Error fetching patients:", error.message)                    
                }
            }
        },
        mounted() {
            this.getPatients()
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