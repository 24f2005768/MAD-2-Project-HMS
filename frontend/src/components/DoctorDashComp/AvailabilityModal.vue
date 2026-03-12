<template>
    <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

    <!-- Modal -->
    <div class="modal fade" id="availModel" tabindex="-1" v-if="availabilityDict">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Availability</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div v-for="date in Object.keys(availabilityDict)" :key= "date" class = "d-flex flex-column px-5">
                        <div>
                            <p class = "mb-1"><strong>{{ date }}</strong></p>
                        </div>
                        <div class = "d-flex justify-content-between mb-2">
                            <div v-for="slot in availabilityDict[date]" :key = "slot" v-on:click="slot.updated_availability == 1 ? slot.updated_availability = 0 : slot.updated_availability = 1" class="card">
                                <!-- if doctor has given previous availability  -->
                                <div class="card-body available" v-if="slot.updated_availability == 1">
                                    <p class="card-title mb-0">{{ slot.name }}: {{ slot.start_time }} - {{ slot.end_time }}</p>
                                </div>

                                <!-- else  -->
                                <div class="card-body unavailable" v-else>
                                    <p class="card-title mb-0">{{ slot.name }}: {{ slot.start_time }} - {{ slot.end_time }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" v-on:click="sendUpdatedStatus">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';
    import errorToast from '@/components/errorToast.vue';

    export default {
        name: "DoctorAvailabilityModal",
        emits: ["error"],
        data() {
            return {
                availabilityDict: null,
                store: useUserStore(),
                errorMessage: ""
            }
        },
        components: {
            errorToast
        },
        methods: {
            async getAvailability() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const availability = await requestAPI("GET", null, `/doctor/availability/${doctorID}`)
                    this.availabilityDict = availability
                }
                catch(error) {
                    // Propagate error to parent (DoctorAvailability)
                    this.$emit('error', error.message)
                }
            },
            async sendUpdatedStatus() {
                try {
                    const doctorID = this.store.user.doctor_id
                    const body = this.availabilityDict
                    const send_updated_availability = await requestAPI("PATCH", body, `/doctor/availability/${doctorID}`)
                    await this.getAvailability()
                }
                catch(error) {
                    // Propagate error to parent (DoctorAvailability)
                    this.$emit('error', error.message)
                }
            }
        },
        mounted() {
            this.getAvailability() 
        }
    }
</script>

<style>
    .available {
        background-color: aqua;
    }
</style>