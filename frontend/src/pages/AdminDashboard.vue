<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Stats</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Patients</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Appointments</button>
                    <button class="nav-link" id="v-tab-main-tab" data-bs-toggle="pill" data-bs-target="#v-tab-main" type="button" role="tab">Doctors</button>
                    <button class="nav-link" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">Departments</button>
                </div>                
            </div>

            <div class = 'col'>
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        Statistics and Charts
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        <AdminDashPatient />
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        <AdminDashAppointment />
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-main" role="tabpanel">
                        <AdminDashDoctor />
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        <AdminDashDept />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import AdminDashDept from '@/components/AdminDashDept.vue';
    import AdminDashDoctor from '@/components/AdminDashDoctor.vue';
    import AdminDashPatient from '@/components/AdminDashPatient.vue';
    import AdminDashAppointment from '@/components/AdminDashAppointment.vue';

    export default {
        name: 'AdminDashboard',
        data() {
            return {}
        },

        components: {
            AdminDashDept,
            AdminDashDoctor,
            AdminDashPatient,
            AdminDashAppointment
        }
    }
</script>

