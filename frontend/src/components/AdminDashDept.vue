<template>
    <div class = 'container'>
        <div class = 'd-flex justify-content-between'>
            <div><h2>Departments</h2></div>
            <div>
                <button class = 'btn btn-primary' type="button" data-bs-toggle="collapse" data-bs-target="#add-dept-button">
                    Add
                </button>
            </div>
        </div>
    </div>

    <div class = 'collapse' id = 'add-dept-button'>
        <div class = 'card card-body'>
            <form>
                <div class = 'row'>
                    <div class = 'row'>
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" placeholder="Department Name*"
                            id="dept_name floatingInput">
                            <label for="dept_name" class="form-label">Name</label>
                        </div> 
                                        
                        <div class="col-md row-sm mb-3 form-floating form-floating">
                            <input type="text" class="form-control" placeholder="User Name*"
                            id="desc floatingInput">
                            <label for="desc" class="form-label">Description</label>
                        </div>               
                    </div>
                    <div class = 'row d-flex flex-column align-items-center'><button type="submit" class="btn btn-primary col-2">Submit</button></div>
                </div>             
            </form>
        </div>
    </div>

    <div class = 'accordion'>
        <div v-for = 'dept in departments' class = 'accordion-item'>
            <h2 class = 'accordion-header'>
                <button class = 'accordion-button' type = 'button' data-bs-toggle = 'collapse' :data-bs-target = '`#${dept.department_id}`'>
                    {{ dept.name }}
                </button>
            </h2>

            <div :id = '`${dept.department_id}`' class = 'accordion-collapse collapse'>
                <div class = 'accordion-body'>
                    <div class = 'conatiner'>
                        <div class = 'd-flex justify-content-between'>
                            <h3 class = 'col-sm-10'>{{ dept.name }}</h3>
                            <div class = 'col'><button type = 'button' class = 'btn btn-primary' data-bs-toggle = "modal" :data-bs-target = '`#update${dept.department_id}`'>Update</button></div>
                            <div class = 'col'><button type = 'button' class = 'btn btn-primary'>Delete</button></div>
                        </div>
                    </div>

                    <p>{{ dept.description }}</p>
                </div>
            </div>

            <div class="modal fade" :id = "`update${dept.department_id}`" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Update Department</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>

                        <div class="modal-body">
                            <form>
                                <div class="col-md row-sm mb-3 form-floating form-floating">
                                    <input type="text" class="form-control" v-model = 'dept.name'
                                    id="floatingInput">
                                    <label for="dept_name" class="form-label">Name</label>
                                </div>

                                <div class="col-md row-sm mb-3 form-floating form-floating">
                                    <textarea class="form-control" v-model = 'dept.description'
                                    id="floatingInput"></textarea>
                                    <label for="desc" class="form-label">Description</label>    
                                </div>                            
                            </form>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Save changes</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../utils/api';

    export default {
        name: 'AdminDashDept',
        data() {
            return {
                departments: []
            }
        },
        methods: {
            async PopulateDept() {
                const all_departments = await requestAPI('GET', null, '/depts')
                this.departments = all_departments
            }
        },
        mounted() {
            this.PopulateDept()
        }
    }
</script>