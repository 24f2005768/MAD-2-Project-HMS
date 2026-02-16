<template>
    <div class = 'container'>
        <div class = "d-flex justify-content-between">
            <h2>Appointments</h2>

            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#bookAppointment" v-on:click="PopulatePatientsDoctors()">
            Book Appointment
            </button>
        </div>
    </div>

    <!-- Add appointment  -->

    <div class="modal fade" id="bookAppointment" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Book Appointment</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <div class="input-group mb-3">
                        <label class="input-group-text" for="inputGroupSelect01">Patients</label>
                        <select class="form-select" id="inputGroupSelect01">
                            <option v-for = "patient in all_patients" :value = "patient.patient_id" v-on:click="selectPatient(patient.patient_id)">{{ patient.name }}</option>
                        </select>
                    </div>

                    <div class="input-group mb-3">
                        <label class="input-group-text" for="inputGroupSelect02">Doctors</label>
                        <select class="form-select" id="inputGroupSelect02">
                            <option v-for = "doctor in all_doctors" :key = "doctor.doctor_id" :value = "doctor.doctor_id" v-on:click="selectDoctor(doctor.doctor_id)">{{ doctor.name }}</option>
                        </select>
                    </div>

                    <div class="input-group mb-3" v-if="doctor">
                        <label class="input-group-text" for="inputGroupSelect03">Date and Shift</label>
                        <select class="form-select" id="inputGroupSelect03">
                            <option v-for = "a in doctor.availability" :value = "a.id" v-on:click="selectAvailability(a.id)">{{ a.date }}  ({{ a.name }})</option>
                        </select>
                    </div>

                    <div class="input-group mb-3" v-show="doctor, shift">
                        <label class="input-group-text" for="inputGroupSelect04">Slot</label>
                        <select class="form-select" id="inputGroupSelect04">
                            <option v-for = "s in shift" :value = "s.id" v-on:click="selectSlot(s.id)">{{ s.start_time }} - {{ s.end_time }}</option>
                        </select>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" v-on:click="ConfirmBooking()">Book</button>
                </div>
            </div>
        </div>
    </div>
    <table class = 'table table-striped table-hover'>
        <thead>
            <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Time</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for = 'a in appointments'>
                <td>{{ a.appointment_id }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.start_time }} - {{ a.end_time }}</td>
                <td>{{ a.app_patient.name }}</td>
                <td>{{ a.app_doctor.name }}</td>
                <td>{{ a.status }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashAppointment',
        data() {
            return {
                appointments: [],
                patient: null,
                doctor: null,
                all_patients: null,
                all_doctors: null,
                shift: null, 
                slot: null
            }
        }, 
        methods: {
            async PopulateAppointments() {
                const all_appointments = await requestAPI('GET', null, '/appointments')
                this.appointments = all_appointments
            },
            
            async PopulatePatientsDoctors() {
                const allPatients = await requestAPI("GET", null, "/patients")
                this.all_patients = allPatients

                const allDoctors = await requestAPI("GET", null, "/doctors")
                this.all_doctors = allDoctors
            },

            async selectPatient(patient_id) {
                const selected_patient = await requestAPI("GET", null, `/patient/${patient_id}`)
                this.patient = selected_patient
            },

            async selectDoctor(doctor_id) {
                const selected_doctor = await requestAPI("GET", null, `/doctor/${doctor_id}?availability=true`)
                this.doctor = selected_doctor
                this.slot = null
            },

            async selectAvailability(id) {
                const selected_shift = await requestAPI("GET", null, `/select-shift/${this.doctor.doctor_id}/${id}`)
                this.shift = selected_shift
            },

            async selectSlot(id) {
                try {
                    const selected_slot = await requestAPI("GET", null, `/book-appointment/${id}`)
                    this.slot = selected_slot
                }
                catch(error) {
                    console.error('Error fetching selected slot', error)
                }
            },

            async ConfirmBooking() {
                try {
                    const data = { 
                        patient_id: this.patient.patient_id
                    }
                    const selected_slot = await requestAPI("PATCH", data, `/book-appointment/${this.slot.id}`)
                    console.log("Successful Booking")
                    this.PopulateAppointments()
                }
                catch(error) {
                    console.log(error)
                    console.error("Error booking an appointment", error)
                }
            }
        },
        mounted() {
            this.PopulateAppointments()
        }
    }
</script>