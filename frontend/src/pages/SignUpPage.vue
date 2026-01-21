<template>
    <h1>This is Sign Up Page</h1>
    <button class = 'btn btn-primary' @click="logoutUser">Logout</button>
</template>

<script>
import { requestAPI } from '../../utils/api';
import { useUserStore } from '@/stores/userStore';

export default {
    name: 'SignUpPage',
    data() {
        return {
            store: useUserStore()
        }
    },

    methods: {
        logoutUser() {
            this.store.logout();
            this.$router.push('/login')
        }
    },
}
</script>