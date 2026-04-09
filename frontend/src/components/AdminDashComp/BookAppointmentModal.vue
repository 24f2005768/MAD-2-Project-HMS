<template>
    <div class="modal fade" id="bookAppointment" tabindex="-1" v-bind="$attrs">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Book Appointment</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div class = "d-flex justify-content-center align-items-center flex-column mb-3">
                        <!-- Profile Pictures  -->
                        <div class = "d-flex justify-content-center w-100">
                            <!-- Patient  -->
                            <div class = "d-flex align-items-center justify-content-center flex-column flex-grow-1" v-if="patient">
                                <div>
                                    <img :src="`/images/${patient.pfp}.png`" height="100px">
                                </div>
                                <div>
                                    <h6>{{ patient.name }}</h6>
                                </div>
                            </div>
                            <!-- Doctor  -->
                            <div class = "d-flex align-items-center justify-content-center flex-column flex-grow-1" v-if="doctor">
                                <div>
                                    <img :src="`/images/${doctor.pfp}.png`" height="100px">
                                </div>
                                <div>
                                    <h6>Dr. {{ doctor.name }}</h6>
                                </div>
                            </div>
                        </div>
                        <!-- Slot  -->
                        <div v-if="slot">
                            <h6>{{ slot.date }} - {{ slot.start_time }} - {{ slot.end_time }} ({{ slot.slots_shifts.name }})</h6>
                        </div>
                    </div>

                    <div class="input-group mb-3">
                        <label class="input-group-text" for="inputGroupSelect01">Patients</label>
                        <select class="form-select" id="inputGroupSelect01" v-model="selectedPatientID">
                            <option selected disabled value="">Please select a patient</option>
                            <template v-for = "patient in all_patients" :key = "patient.patient_id">
                                <option v-if="patient.patient_user.blacklisted == false" :value = "patient.patient_id">{{ patient.name }}</option>
                                <option disabled="" v-if="patient.patient_user.blacklisted == true">{{ patient.name }}</option>
                            </template>
                        </select>
                    </div>

                    <div class="input-group mb-3">
                        <label class="input-group-text" for="inputGroupSelect02">Doctors</label>
                        <select class="form-select" id="inputGroupSelect02" v-model="selectedDoctorID">
                            <option selected disabled value="">Please select a doctor</option>
                            <template v-for = "doctor in all_doctors" :key = "doctor.doctor_id">
                                <option v-if="doctor.doctor_user.blacklisted == false" :value = "doctor.doctor_id">{{ doctor.name }}</option>
                                <option disabled="" v-if="doctor.doctor_user.blacklisted == true">{{ doctor.name }}</option>
                            </template>
                        </select>
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
                                <option v-if="s.doctor_free === true" :value="s.id">
                                    {{ s.start_time }} - {{ s.end_time }} (Available)
                                </option>
                                <option v-else disabled :value="s.id" class="text-muted">
                                    {{ s.start_time }} - {{ s.end_time }} (Booked)
                                </option>
                            </template>
                        </select>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button v-if="doctor && slot && shift" type="button" class="btn btn-outline-primary" v-on:click="ConfirmBooking()">Book</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: 'BookAppointmentModal',
        emits: ['error', 'success'],
        data() {
            return {
                store: useUserStore(),
                appointments: [],
                doctor: null,
                patient: null,
                all_doctors: null,
                all_patients: null,
                shift: null, 
                slot: null,
                selectedDoctorID: "",
                selectedPatientID: "",
                selectedShiftID: "",
                selectedSlotID: ""
            }
        }, 
        methods: {
            async PopulateDoctors() {
                const allDoctors = await requestAPI("GET", null, "/doctors")
                this.all_doctors = allDoctors
            },
            async PopulatePatients() {
                const allPatients = await requestAPI("GET", null, "/patients")
                this.all_patients = allPatients
            },
            async ConfirmBooking() {
                try {
                    const data = { 
                        patient_id: this.selectedPatientID
                    }
                    const selected_slot = await requestAPI("PATCH", data, `/book-appointment/${this.slot.id}`)
                    this.$emit("success", "Appointment booked successfully!")
                    bootstrap.Modal.getInstance(document.getElementById("bookAppointment")).hide()
                }
                catch(error) {
                    console.log(error)
                    this.$emit("error", error.message)
                }
            },
            async selectPatient(patient_id) {
                const selected_patient = await requestAPI("GET", null, `/patient/${patient_id}`)
                this.patient = selected_patient
            },
        },
        watch: {
            async selectedDoctorID(newVal, oldVal) {
                this.shift = null
                this.slot = null
                this.selectedShiftID = ''
                this.selectedSlotID = ''

                if (newVal) {
                    const selected_doctor = await requestAPI("GET", null, `/doctor/${newVal}?availability=true`)
                    this.doctor = selected_doctor
                }
            },
            async selectedPatientID(newVal, oldVal) {
                // this.selectedPatientID = ""

                if (newVal) {
                    const selected_patient_modal = await requestAPI("GET", null, `/patient/${newVal}`)
                    this.patient = selected_patient_modal
                }
            },
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
                        this.$emit("error", error.message)
                    }
                }
            }
        },
        mounted() {
            this.PopulateDoctors(),
            this.PopulatePatients()
        }
    }
</script>