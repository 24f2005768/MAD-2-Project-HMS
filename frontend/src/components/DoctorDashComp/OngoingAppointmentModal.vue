<template>
    <div class = "modal fade" tabindex = "-1" :id="`ongoing-appt-modal-${appointmentID}`">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Give Appointment Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form @submit.prevent = "giveTreatment">
                    <div class="modal-body">
                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "diagnosis"
                            id="floatingInput">
                            <label for = "diagnosis" class = "form-label">Diagnosis</label>
                        </div> 

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "notes"
                            id="floatingInput">
                            <label for = "notes" class = "form-label">Notes</label>
                        </div>  

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "prescription"
                            id="floatingInput">
                            <label for = "prescription" class = "form-label">Prescription</label>
                        </div>  

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "tests"
                            id="floatingInput">
                            <label for = "tests" class = "form-label">Tests</label>
                        </div>  

                    </div>
                    
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-outline-primary">Save changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        "name": "OngoingAppointmentModal",
        emits: ["error"],
        data() {
            return {
                diagnosis: null, 
                notes: null,
                prescription: null,
                tests: null
            }
        },
        props: {
            appointmentID: {
                type: [Number, String],
                required: true
            }
        },
        emits: ["treatment", "error"],
        methods: {
            async giveTreatment() {
                try {
                    const data = {
                        diagnosis: this.diagnosis, 
                        notes: this.notes,
                        prescription: this.prescription,
                        tests: this.tests
                    }
                    this.$emit("treatment", data)  
                    bootstrap.Modal.getInstance(document.getElementById(`ongoing-appt-modal-${this.appointment_id}`)).hide()                 
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            }
        }
    }
</script>