<template>
    <div class="modal fade" id="addDeptModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Doctor</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <form @submit.prevent = "SubmitAddDepartmentForm">
                    <div class="modal-body">
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model="name"
                            id="dept_name floatingInput">
                            <label for="dept_name" class="form-label">Name*</label>
                        </div> 
                                        
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" v-model="description"
                            id="desc floatingInput">
                            <label for="desc" class="form-label">Description</label>
                        </div>                        
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-outline-primary">Add Department</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: 'AddDepartmentModal',
        data() {
            return {
                name: '',
                description: '',
             }
        },
        emits: ["error", "form-add-department"],
        methods: {
            async SubmitAddDepartmentForm() {
                try {
                    const data = {
                        name: this.name,
                        description: this.description,
                    }
                    this.$emit("form-add-department", data)
                    bootstrap.Modal.getInstance(document.getElementById("addDeptModal")).hide()
                }
                catch(error) {
                    this.$emit("error", error.message)
                }
            }
        }
    }
</script>