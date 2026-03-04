<template>
    <div class = "toast-container position-fixed bottom-0 end-0 p-5">
        <div v-if="show" class="toast show bottom-0" role="alert">
            <div class="toast-header">
                <h3>Error</h3>
            </div>

            <div class="toast-body">
                {{ message }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "errorToast",
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
            // Reset show when message changes
            message: {
                immediate: true,
                handler() {
                    this.show = true;
                }
            }
        }
    }
</script>