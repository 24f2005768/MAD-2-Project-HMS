<template>
    <div class = "modal fade" tabindex = "-1" id="update-treatment-modal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Give Appointment Details</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form @submit.prevent = "updateTreatment">
                    <div class="modal-body">
                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "appointment.app_t.diagnosis"
                            id="floatingInput">
                            <label for = "diagnosis" class = "form-label">Diagnosis</label>
                        </div> 

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "appointment.app_t.notes"
                            id="floatingInput">
                            <label for = "notes" class = "form-label">Notes</label>
                        </div>  

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "appointment.app_t.prescription"
                            id="floatingInput">
                            <label for = "prescription" class = "form-label">Prescription</label>
                        </div>  

                        <div class = "col-md row-sm mb-3 form-floating form-floating">
                            <input type = "text" class = "form-control" v-model = "appointment.app_t.tests"
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
        "name": "UpdateTreatmentModal",
        data() {
            return {
                diagnosis: "", 
                notes: "",
                prescription: "",
                tests: ""
            }
        },
        props: {
            appointment: {
                type: Object,
                required: true
            }
        },
        emits: ["update-treatment", "error"],
        methods: {
            async updateTreatment() {
                try {
                    const data = {
                        diagnosis: this.appointment.app_t.diagnosis, 
                        notes: this.appointment.app_t.notes,
                        prescription: this.appointment.app_t.prescription,
                        tests: this.appointment.app_t.tests
                    }
                    this.$emit("update-treatment", data)                   
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            }
        }
    }
</script>