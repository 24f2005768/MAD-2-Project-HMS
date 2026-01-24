<template>
    <div class = 'container-fluid d-flex justify-content-center align-items-center'>
        <div class = 'row d-flex flex-column justify-content-center'>
            <form @submit.prevent="loginUser">
            <div class="mb-3">
                <label for="user_name" class="form-label">User Name</label>
                <input type="text" class="form-control" 
                id="user_name" v-model ="user_name">
            </div>

            <div class="mb-3">
                <label for="user_password" class="form-label">User Password</label>
                <input type="password" class="form-control" 
                id="user_password" v-model = "user_password">
            </div>
            
            <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
import { requestAPI } from '../../utils/api';
import { useUserStore } from '@/stores/userStore';

export default {
    name: 'LoginPage',
    data() {
        return {
            store: useUserStore(),
            user_name: '',
            user_password: ''
        }
    },

    methods: {
        async loginUser() {
            const request = await this.store.login({
                'user_name': this.user_name,
                'user_password': this.user_password
            })
            console.log(request)
            if (this.store.role == 'Admin') {
                this.$router.push('/admin')
            }
            if (this.store.role == 'Doctor') {
                this.$router.push('/doctor')
            }
            if (this.store.role == 'Patient') {
                this.$router.push('/patient')
            }
        }
    },
}
</script>
