<template>
    <nav class = 'navbar header'>
        <div class="container-fluid">
            <div class = 'navbar-brand' style="color: white" v-on:click="goToDashboard">LDH Hospital</div>

            <!-- only show to users after they login in  -->
            <div class = 'd-flex gap-2' v-if="store.user">
                <form class ="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" v-model="searchItem">
                    <button class="btn btn-outline-success" type="submit" @click.prevent = "search">
                        Search
                    </button>
                </form>

                <button type="button" class="btn btn-outline-secondary" v-on:click="logout">
                    <i class="bi bi-box-arrow-right"></i> Logout
                </button>
            </div>
        </div>
    </nav>
</template>

<script>
    import { requestAPI } from '../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    export default {
        name: "Header",
        data() {
            return {
                store: useUserStore(),
                searchItem: null,
                errorMessage: ""
            }
        },
        methods: {
            search() {
                const role = this.store.role 
                try {
                    this.$router.push(
                        role === "Admin" ? `/admin/search/${this.searchItem}` :
                        role === "Doctor" ? `/doctor/search/${this.searchItem}` :
                        role === "Patient" ? `/patient/search/${this.searchItem}` :
                        "/login"
                    )
                }
                catch(error) {
                    this.errorHandler(error.message);
                }
            },

            goToDashboard() {
                if (!this.store.user) {
                    this.$router.push("/login")
                }

                const role = this.store.role
                this.$router.push(
                    role === "Admin" ? "/admin" :
                    role === "Doctor" ? "/doctor" :
                    role === "Patient" ? "/patient" :
                    "/login"
                )
            },

            errorHandler(message) {
                this.errorMessage = message;
            },

            async logout() {
                const logout_user = await (requestAPI("POST", null, "/logout"))
                this.store.logout();
                this.$router.push("/login")
            }
        }
    }
</script>

<style>
    .header {
        background-color: #313866;
        padding-left: 15px;
        width: 100vw;
        top: 0;
        /* position: fixed; */
        margin-top: 0px;
        color: white;
        filter: drop-shadow(2px 2px 3px rgba(0, 0, 0, 0.8));
        font-family: "Montserrat", sans-serif;
        display: flex;
        justify-content: space-between;
        }
</style>