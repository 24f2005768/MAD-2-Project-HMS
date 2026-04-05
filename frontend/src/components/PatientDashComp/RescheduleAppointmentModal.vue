<template>
    <div class="modal fade" :id="`rescheduleAppointment-${appointment_id}`" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Reschedule Appointment</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div class = "d-flex justify-content-center align-items-center flex-column mb-3">
                        <div v-if="doctor">
                            <img :src="`/images/${doctor.pfp}.png`" height="100px">
                        </div>
                        <div v-if="doctor">
                            <h6>Dr. {{ doctor.name }}</h6>
                        </div>
                        <div v-if="slot">
                            <h6>{{ slot.date }} - {{ slot.start_time }} - {{ slot.end_time }} ({{ slot.slots_shifts.name }})</h6>
                        </div>
                    </div>

                    <div class="input-group mb-3" v-if="doctor">
                        <label class="input-group-text" for="inputGroupSelect03">Date and Shift</label>
                        <select class="form-select" id="inputGroupSelect03" v-model="selectedShiftID">
                            <option selected disabled value="">Please select a date and shift</option>
                            <option v-for = "a in doctor.availability" :value = "a.id">{{ a.date }}  ({{ a.name }})</option>
                        </select>
                    </div>

                    <div class="input-group mb-3" v-show="doctor, shift">
                        <label class="input-group-text" for="inputGroupSelect04">Slot</label>
                        <select class="form-select" id="inputGroupSelect04" v-model="selectedSlotID">
                            <option selected disabled value="">Please select a slot</option>
                            <template v-for="s in shift" :key="s.id">
                                <option v-if="s.doctor_free === true && s.patient_free === true" :value="s.id">
                                    {{ s.start_time }} - {{ s.end_time }} (Available)
                                </option>
                                <option v-else-if="s.patient_free === false && s.doctor_free === true" disabled :value="s.id" class="text-muted">
                                    {{ s.start_time }} - {{ s.end_time }} (You have an appointment)
                                </option>
                                <option v-else-if="s.doctor_free === false && s.patient_free === true" disabled :value="s.id" class="text-muted">
                                    {{ s.start_time }} - {{ s.end_time }} (Booked)
                                </option>
                            </template>
                        </select>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button v-if="doctor && slot && shift" type="button" class="btn btn-outline-primary" v-on:click="ConfirmReschedule()">Reschedule</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: 'RescheduleAppointmentModal',
        emits: ['error', 'success'],
        props: {
            doctor_id: {
                type: Number,
                required: true
            },
            appointment_id: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                store: useUserStore(),
                appointments: [],
                doctor: null,
                // all_doctors: null,
                shift: null, 
                slot: null,
                // selectedDoctorID: "",
                selectedShiftID: "",
                selectedSlotID: ""
            }
        }, 
        methods: {
            async getDoctor() {
                const doc = await requestAPI("GET", null, `/doctor/${this.doctor_id}?availability=true`)
                this.doctor = doc;
            },
            async ConfirmReschedule() {
                try {
                    const data = { 
                        patient_id: this.store.user.patient_id,
                        slot_id: this.selectedSlotID
                    }
                    const selected_slot = await requestAPI("PATCH", data, `/reschedule-appointment/${this.appointment_id}`)
                    if (selected_slot) {
                        this.$emit('success', 'Your appointment was rescheduled successfully!')
                    }
                }
                catch(error) {
                    this.$emit('error', error.message)
                }
            }
        },
        watch: {
            async selectedShiftID(newVal, oldVal) {
                this.shift = null
                this.slot = null
                this.selectedSlotID = ''

                if (newVal && this.doctor) {
                    // Fetch available slots for selected shift
                    const selected_shift = await requestAPI("GET", null, `/select-shift/${this.doctor.doctor_id}/${newVal}`)
                    this.shift = selected_shift
                }
            },
            async selectedSlotID(newVal, oldVal) {
                // Reset slot when new slot is selected
                this.slot = null
                
                if (newVal) {
                    try {
                        const selected_slot = await requestAPI("GET", null, `/book-appointment/${newVal}`)
                        this.slot = selected_slot
                    } catch(error) {
                        console.error('Error fetching selected slot', error)
                    }
                }
            }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>