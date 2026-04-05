<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist">
                    <button class="nav-link active border-bottom" @click="tabshown = 'home'" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Home
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'stats'" id="v-tab-stats-tab" data-bs-toggle="pill" data-bs-target="#v-tab-stats" type="button" role="tab">
                        Stats
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'doctors'" id="v-tab-doctors-tab" data-bs-toggle="pill" data-bs-target="#v-tab-doctors" type="button" role="tab">
                        Doctors
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'appts'" id="v-tab-appt-tab" data-bs-toggle="pill" data-bs-target="#v-tab-appt" type="button" role="tab">
                        Appointments
                    </button>
                </div>                
            </div>

            <div class = 'col'>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex" id="v-tab-tabContent" style="margin: 30px;">
                    
                    <!-- Home  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <PatientProfile @error = "errorHandler" @success="successHandler"/>
                    </div>

                    <!-- Stats -->
                    <div class="tab-pane fade w-100" id="v-tab-stats" role="tabpanel">
                        <PatientDashCharts @error = "errorHandler"/>
                    </div>

                    <!-- Patients  -->
                    <div class="tab-pane fade w-100" id="v-tab-doctors" role="tabpanel">
                        <PatientDashDoctors @error = "errorHandler" @success="successHandler"/>
                    </div>

                    <!-- Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-appt" role="tabpanel">
                        <PatientDashAppointments @error = "errorHandler" @success="successHandler"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import errorToast from '@/components/errorToast.vue';
    import successToast from '@/components/successToast.vue';
    
    import PatientProfile from '@/components/PatientDashComp/PatientProfile.vue';
    import PatientDashDoctors from '@/components/PatientDashComp/PatientDashDoctors.vue';
    import PatientDashAppointments from '@/components/PatientDashComp/PatientDashAppointments.vue';
    import PatientDashCharts from '@/components/PatientDashComp/PatientDashCharts.vue';
    
    export default {
        name: 'PatientDash',
        data() {
            return {
                errorMessage: "",
                successMessage: "",
                tabshown: 'home',
            }
        },
        components: {
            errorToast,
            successToast,
            PatientProfile,
            PatientDashDoctors,
            PatientDashAppointments,
            PatientDashCharts
        },
        methods: {
            errorHandler(message) {
                this.errorMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.errorMessage = '';
                }, 5000);
            },
            successHandler(message) {
                this.successMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.successMessage = '';
                }, 5000);
            }
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        border-bottom: 2px solid orangered !important;
    }
</style>