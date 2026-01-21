<template>
    <div class = 'container-fluid d-flex justify-content-center align-items-center'>
        <div class = 'row d-flex flex-column justify-content-center'>
            <form @submit.prevent ="">
            <div class="mb-3">
                <label for="user_name" class="form-label">User Name</label>
                <input type="text" class="form-control" placeholder="User Name"
                id="user_name">
            </div>

            <div class="mb-3">
                <label for="user_password" class="form-label">User Password</label>
                <input type="password" class="form-control" placeholder="User Password"
                id="user_password">
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" placeholder="User Name"
                id="email">
            </div>

            <div class="mb-3">
                <label for="contact_number" class="form-label">Contact Number</label>
                <input type="tel" class="form-control" placeholder="User Name"
                id="contact_number">
            </div>


            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" placeholder="Name"
                id="name">
            </div>

            <div class="mb-3">
                <label for="dob" class="form-label">DOB</label>
                <input type="date" class="form-control" 
                id="dob">
            </div>

            <div class="mb-3">
                <label for="gender" class="form-label">Gender</label>              
                <select class="form-select" aria-label="Default select example">
                    <option selected>Select your gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="height" class="form-label">Height in cm</label>
                <input type="number" class="form-control" placeholder="Height" min="0"
                id="height">
            </div>

            <div class="mb-3">
                <label for="weight" class="form-label">Weight in kg</label>
                <input type="number" class="form-control" placeholder="Weight" min="0"
                id="weight">
            </div>
            
            <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>