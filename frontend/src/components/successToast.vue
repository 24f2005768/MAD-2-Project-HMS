<template>
    <div class = "toast-container position-fixed bottom-0 end-0 p-5">
        <div v-if="show" class = "toast show bottom-0" role="alert">
            <div class = "toast-header bg-success text-white">
                <p class = "mb-0">Success</p>
                <button type="button" class="btn-close btn-close-white ms-auto" @click="show = false"></button>
            </div>

            <div class="toast-body">
                {{ message }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "successToast",
        props: {
            message: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                show: true
            }
        },
        watch: {
            message() {
                this.show = true;
            }
        }
    }
</script>