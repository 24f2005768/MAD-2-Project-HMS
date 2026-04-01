<template>
    <div class = "text-center mb-2 border-bottom">
        <h5 v-if="countsData">{{ countsData.patients }} Patients, {{ countsData.appointments }} Appointments,
            {{ countsData.doctors }} Doctors, {{ countsData.departments }} Departments
        </h5>
    </div>
    <div class = "d-flex flex-wrap justify-content-center align-items-center gap-4" style="min-height: 80vh;">
        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 flex-grow-1" style="max-width:380px; height:250px">
            <canvas id="appointmentsByMonthChart">
            </canvas>
            <h6>Month wise distribution of Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2" style="max-width:380px;">
            <div style="height: 200px;">
                <canvas id="appointmentsByDeptChart" style="width:100%; height:100%;">
                </canvas>
            </div>
            <h6>Department wise distribution of Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2" style="max-width:380px;">
            <div style="height: 200px;">
                <canvas id="doctorsByDeptChart" style="width:100%; height:100%;">
                </canvas>
            </div>
            <h6>Department wise distribution of Doctors</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2" style="max-width:380px;">
            <div style="height: 200px;">
                <canvas id="patientsByGenderChart" style="width:100%; height:100%;">
                </canvas>
            </div>
            <h6>Gender distribution of Patients</h6>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { Chart } from 'chart.js/auto';

    export default {
        name: "AdminDashCharts",
        data() {
            return {
                appointmentsByMonthData: null,
                appointmentsByMonthChart: null,
                appointmentsByDeptData: null, 
                appointmentsByDeptChart: null, 
                doctorsByDeptData: null,
                doctorsByDeptChart: null,
                patientsByGenderData: null,
                patientsByGenderChart: null,
                countsData: null,
                errorMessage: null,
            }
        },
        emits: ["error"],
        methods: {
            async getCharts() {
                try {
                    const results = await requestAPI("GET", null, "/admin/charts")
                    
                    // Chart 1
                    this.appointmentsByMonthData = results.appointments_by_month
                    const ctx1 = document.getElementById('appointmentsByMonthChart').getContext('2d');
                    const months = Object.keys(this.appointmentsByMonthData)
                    const apptCountByMonth = Object.values(this.appointmentsByMonthData)

                    this.appointmentsByMonthChart = new Chart(ctx1, {
                        type: "bar",
                        data: {
                            labels: months,
                            datasets: [{
                                label: "Appointments by Month",
                                data: apptCountByMonth,
                                backgroundColor: [
                                    'rgba(255, 99, 132, 1)',  
                                    'rgba(54, 162, 235, 1)',   
                                    'rgba(255, 206, 86, 1)',   
                                    'rgba(75, 192, 192, 1)',   
                                    'rgba(153, 102, 255, 1)',  
                                    'rgba(255, 159, 64, 1)'    
                                ],
                                borderColor: [
                                    'rgba(255, 99, 132, 1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)',
                                    'rgba(153, 102, 255, 1)',
                                    'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            maintainAspectRatio: true,
                        }
                    })
                    
                    // Chart 2
                    this.appointmentsByDeptData = results.appointments_by_dept
                    const ctx2 = document.getElementById('appointmentsByDeptChart').getContext('2d')
                    const apptDepartments = Object.keys(this.appointmentsByDeptData)
                    const apptDepartmentsCount = Object.values(this.appointmentsByDeptData)

                    this.appointmentsByDeptChart = new Chart(ctx2, {
                        type: "pie",
                        data: {
                            labels: apptDepartments,
                            datasets: [{
                                label: "Appointments",
                                data: apptDepartmentsCount,
                            }],
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            animation: {
                                duration: 1200,      
                                easing: 'easeOutQuart',
                                animateRotate: true, 
                                animateScale: true   
                            },
                        }
                    })

                    // Chart 3
                    this.doctorsByDeptData = results.doctors_by_dept
                    const ctx3 = document.getElementById('doctorsByDeptChart').getContext('2d')
                    const doctorDepartments = Object.keys(this.doctorsByDeptData)
                    const doctorDepartmentsCount = Object.values(this.doctorsByDeptData)

                    this.doctorsByDeptChart = new Chart(ctx3, {
                        type: "pie",
                        data: {
                            labels: doctorDepartments,
                            datasets: [{
                                label: "Doctors",
                                data: doctorDepartmentsCount,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            animation: {
                                duration: 1200,      
                                easing: 'easeOutQuart',
                                animateRotate: true, 
                                animateScale: true   
                            },
                        }
                    })

                    // Chart 4
                    this.patientsByGenderData = results.patients_by_gender
                    const ctx4 = document.getElementById('patientsByGenderChart').getContext('2d')
                    const genders = Object.keys(this.patientsByGenderData)
                    const genderCount = Object.values(this.patientsByGenderData)

                    this.patientsByGenderChart = new Chart(ctx4, {
                        type: "pie",
                        data: {
                            labels: genders,
                            datasets: [{
                                label: "Gender",
                                data: genderCount,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            animation: {
                                duration: 1200,      
                                easing: 'easeOutQuart',
                                animateRotate: true, 
                                animateScale: true   
                            },
                        }
                    })

                    // Count 
                    this.countsData = results.count
                }
                catch(error) {
                    this.$emit("error")
                }
            }
        },
        mounted() {
            this.getCharts()
        }
    }
</script>