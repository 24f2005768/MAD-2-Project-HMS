<template>
    <nav class = 'navbar header'>
        <div class="container-fluid">
            <div class = 'navbar-brand' style="color: white;margin-left: 3px;">LDH Hospital</div>
            <div class = 'd-flex gap-2'>
                <form class ="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" v-model="searchItem">
                    <button class="btn btn-outline-success" type="submit" v-on:click="search">Search</button>
                </form>
                <a>Logout</a>
            </div>
        </div>
    </nav>
</template>

<script>
    export default {
        name: "Header",
        data() {
            return {
                searchItem: null
            }
        },

        methods: {
            async search() {
                this.$router.push(`/admin/search/${this.searchItem}`)
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