<template>
    <div class="container d-flex align-items-start flex-grow-1 min-vh-80 min-vw-80">
        <h3>View doctor</h3>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';

    export default {
        name: 'ViewDoctor',
        data() {
            return {
                doctor: null,
            }
        },
        methods: {
            async getDoctor() {
                const doctorId = this.$route.params.did;
                const display_doctor = await requestAPI('GET', null, `/doctor/${doctorId}`)
                this.doctor = display_doctor
            }
        },
        mounted() {
            this.getDoctor()
        }
    }
</script>