<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-90 min-vw-100">
        <div class = 'container'>
            <div class = 'col'>
                <div class="nav nav-tab me-3 my-auto d-flex align-items-center justify-content-center" id="v-tab-tab" role="tablist" aria-orientation="vertical">
                    <button class="nav-link active" id="v-tab-home-tab" data-bs-toggle="pill" data-bs-target="#v-tab-home" type="button" role="tab">Availability</button>
                    <button class="nav-link" id="v-tab-profile-tab" data-bs-toggle="pill" data-bs-target="#v-tab-profile" type="button" role="tab">Upcoming Appointments</button>
                    <button class="nav-link" id="v-tab-messages-tab" data-bs-toggle="pill" data-bs-target="#v-tab-messages" type="button" role="tab">Past Appointments</button>
                    <button class="nav-link" id="v-tab-settings-tab" data-bs-toggle="pill" data-bs-target="#v-tab-settings" type="button" role="tab">Departments</button>
                </div>                
            </div>

            <div class = 'col'>
                <h2>Profile</h2>

                <!-- Always visible -->
                <div class = 'container'>
                    <div class = 'row'>
                        
                    </div>
                </div>

                <!-- Conditional Rendering -->
                <div class="tab-content d-flex flex-grow-1" id="v-tab-tabContent">
                    
                    <!-- Availability  -->
                    <div class="tab-pane fade show active w-100" id="v-tab-home" role="tabpanel">
                        First
                    </div>

                    <!-- Upcoming Appointments -->
                    <div class="tab-pane fade w-100" id="v-tab-profile" role="tabpanel">
                        Second
                    </div>

                    <!-- Past Appointments  -->
                    <div class="tab-pane fade w-100" id="v-tab-messages" role="tabpanel">
                        Third
                    </div>

                    <div class="tab-pane fade w-100" id="v-tab-settings" role="tabpanel">
                        Fourth
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>