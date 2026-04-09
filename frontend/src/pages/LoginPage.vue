<template>       
    <div class="container d-flex flex-column align-items-center justify-content-center flex-grow-1 min-vw-100 gap-3" style="min-height: 90vh;">
        <errorToast v-if="errorMessage" :message="errorMessage" @close="errorMessage = ''"/>

        <div class = "w-100 d-flex justify-content-center">
            <h3 class>Login</h3>
        </div>

        <div class = 'card row d-flex flex-column justify-content-center align-items-center gap-2 p-2 w-50'>
            <form @submit.prevent="loginUser">
                <div class="mb-3 mt-3">
                    <label for="user_name" class="form-label">User Name</label>
                    <input type="text" class="form-control" 
                    id="user_name" v-model ="user_name">
                </div>

                <div class="mb-3 mt-3">
                    <label for="user_password" class="form-label">User Password</label>
                    <input type="password" class="form-control" 
                    id="user_password" v-model = "user_password">
                </div>
                
                <div class = "w-100 d-flex justify-content-center mb-3">
                    <button type="submit" class="btn btn-outline-danger">Submit</button>
                </div>
            </form>
        </div>

        <div class = "w-100 d-flex justify-content-center">
            <p>Not a member? <RouterLink to="/register">Sign up</RouterLink> instead</p>
        </div>
    </div>
</template>

<script>
import { requestAPI } from '../../utils/api';
import { useUserStore } from '@/stores/userStore';
import errorToast from '@/components/errorToast.vue';

export default {
    name: 'LoginPage',
    data() {
        return {
            store: useUserStore(),
            user_name: '',
            user_password: '',
            errorMessage: ''
        }
    },
    components: {
        errorToast
    },
    methods: {
        async loginUser() {
            try {
                const request = await this.store.login({
                    'user_name': this.user_name,
                    'user_password': this.user_password
                })
                
                if (this.store.role == 'Admin') {
                    this.$router.push('/admin')
                }
                if (this.store.role == 'Doctor') {
                    this.$router.push(`/doctor`)
                }
                if (this.store.role == 'Patient') {
                    this.$router.push(`/patient`)
                }
            }
            catch(error) {
                    this.errorHandler(error.message);
                }
            },
            errorHandler(message) {
                this.errorMessage = message;
                // Auto clear success after 5 seconds
                setTimeout(() => {
                    this.errorMessage = '';
                }, 5000);
            },
        }
    }

</script>

<style scoped>
    .card {
        background-color: #f5cdcd;
    }
    input {
        background-color: #f5eeee;
    }
</style>