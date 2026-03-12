<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist">
                    <button class="nav-link active border-bottom" @click="tabshown = 'home'" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Home
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'stats'" id="v-tab-stats-tab" data-bs-toggle="pill" data-bs-target="#v-tab-stats" type="button" role="tab">
                        Stats
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'patients'" id="v-tab-patients-tab" data-bs-toggle="pill" data-bs-target="#v-tab-patients" type="button" role="tab">
                        Patients
                    </button>

                    <button class="nav-link border-bottom" @click="tabshown = 'appts'" id="v-tab-appt-tab" data-bs-toggle="pill" data-bs-target="#v-tab-appt" type="button" role="tab">
                        Appointments & Availability
                    </button>
                </div>                
            </div>

            <div class = 'col'>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex" id="v-tab-tabContent" style="margin: 30px;">
                    
                    <!-- Home  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <DoctorProfile v-if="tabshown == 'home'" @error = "errorHandler"/>
                    </div>

                    <!-- Stats -->
                    <div class="tab-pane fade w-100" id="v-tab-stats" role="tabpanel">
                        Second v-show="tabshown == 'stats'" 
                    </div>

                    <!-- Patients  -->
                    <div class="tab-pane fade w-100" id="v-tab-patients" role="tabpanel">
                        <DoctorDashPatients v-show="tabshown == 'patients'" />
                    </div>

                    <!-- Availability and Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-appt" role="tabpanel">
                        <DoctorAvailability v-if="tabshown == 'appts'" @error="errorHandler"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import errorToast from '@/components/errorToast.vue';
    
    import DoctorDashPatients from '@/components/DoctorDashComp/DoctorDashPatients.vue';
    import DoctorProfile from '@/components/DoctorDashComp/DoctorProfile.vue';
    import DoctorAvailability from '@/components/DoctorDashComp/DoctorAvailability.vue';
    
    export default {
        name: 'DoctorDash',
        data() {
            return {
                errorMessage: "",
                tabshown: 'home'
            }
        },
        components: {
            errorToast,
            DoctorProfile,
            DoctorDashPatients,
            DoctorAvailability
        },
        methods: {
            errorHandler(message) {
                this.errorMessage = message
            }
        }
    }
</script>

<style scoped>
    .nav-tab .nav-link.active {
        /* background-color: rgba(0, 0, 0, 0.175) !important; */
        border-bottom: 2px solid orangered !important;
    }
</style>