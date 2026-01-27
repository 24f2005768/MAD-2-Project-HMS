<template>
    <nav class = 'd-flex justify-content-space-between navbar navbar-expand-lg header'>
        <div class = 'navbar-brand' style="color: white;margin-left: 3px;">LDH Hospital</div>
        <div class="container-fluid">
            <form class="d-flex">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
        </div>
    </nav>
</template>

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