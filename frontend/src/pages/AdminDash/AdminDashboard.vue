<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>
        <successToast v-if="successMessage" :message="successMessage" @close="successMessage = ''"/>

        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">
                        Stats
                    </button>
                    
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">
                        Patients
                    </button>

                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">
                        Appointments
                    </button>

                    <button class="nav-link" id="v-tab-main-tab" data-bs-toggle="pill" data-bs-target="#v-tab-main" type="button" role="tab">
                        Doctors
                    </button>

                    <button class="nav-link" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">
                        Departments
                    </button>

                </div>                
            </div>

            <div class = 'col'>
                <div class = "w-100 d-flex justify-content-end mb-3">
                    <!-- <button type = "button" class="btn btn-outline-secondary" onclick = 'history.back()'>Go Back</button> -->
                </div>

                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        <AdminDashCharts @error = "errorHandler"/>
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <AdminDashPatient @error = "errorHandler" @success="successHandler"/>
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <AdminDashAppointment @error = "errorHandler" @success="successHandler"/>
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-main" role="tabpanel">
                        <AdminDashDoctor @error = "errorHandler" @success="successHandler"/>
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        <AdminDashDept @error = "errorHandler" @success="successHandler"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import errorToast from '@/components/errorToast.vue';
    import successToast from '@/components/successToast.vue';

    import AdminDashDept from '@/components/AdminDashComp/AdminDashDept.vue';
    import AdminDashDoctor from '@/components/AdminDashComp/AdminDashDoctor.vue';
    import AdminDashPatient from '@/components/AdminDashComp/AdminDashPatient.vue';
    import AdminDashAppointment from '@/components/AdminDashComp/AdminDashAppointment.vue';
    import AdminDashCharts from '@/components/AdminDashComp/AdminDashCharts.vue';

    export default {
        name: 'AdminDashboard',
        data() {
            return {
                errorMessage: '',
                successMessage: ''
            }
        },

        components: {
            AdminDashDept,
            AdminDashDoctor,
            AdminDashPatient,
            AdminDashAppointment,
            AdminDashCharts,
            errorToast,
            successToast
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
        /* background-color: rgba(0, 0, 0, 0.175) !important; */
        border-bottom: 2px solid orangered !important;
    }
</style>