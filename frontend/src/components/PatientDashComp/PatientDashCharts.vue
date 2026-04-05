<template>
    <div class = "d-flex flex-wrap justify-content-evenly align-items-center gap-5" style="min-height: 80vh;">
        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 text-center">
            <canvas id="appointmentsByMonthChart">
            </canvas>
            <h6>Month wise distribution of Appointments</h6>
        </div>
    
        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="thisMonthAppointmentsByDeptChart">
                </canvas>
            <!-- </div> -->
            <h6>Doctor wise distribution of this Month's Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="thisMonthAppointmentsBydoctorsChart">
                </canvas>
            <!-- </div> -->
            <h6>Doctor wise distribution of this Month's Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="overallAppointmentsByDeptChart">
                </canvas>
            <!-- </div> -->
            <h6>Department wise distribution of all Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="overallAppointmentsBydoctorsChart">
                </canvas>
            <!-- </div> -->
            <h6>Doctor wise distribution of all Appointments</h6>
        </div>
    </div>
</template>

<script>
    import { requestAPI } from '../../../utils/api';
    import { useUserStore } from '@/stores/userStore';

    import { Chart } from 'chart.js/auto';

    export default {
        name: "PatientDashCharts",
        data() {
            return {
                store: useUserStore(),

                appointmentsByMonthData: null,
                appointmentsByMonthChart: null,

                overallAppointmentsByDeptData: null, 
                overallAppointmentsByDeptChart: null,

                thisMonthAppointmentsByDeptData: null, 
                thisMonthAppointmentsByDeptChart: null, 

                overallAppointmentsBydoctorsData: null,
                overallAppointmentsBydoctorsChart: null,

                thisMonthAppointmentsBydoctorsData: null,
                thisMonthAppointmentsBydoctorsChart: null,
            }
        },
        emits: ["error"],
        methods: {
            async getCharts() {
                try {
                    const patientID = this.store.user.patient_id;
                    const results = await requestAPI("GET", null, `/patient/charts/${patientID}`)
                    
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
                    this.overallAppointmentsByDeptData = results.overall_appt_by_dept
                    const ctx2 = document.getElementById('overallAppointmentsByDeptChart').getContext('2d')
                    const overallApptDepartments = Object.keys(this.overallAppointmentsByDeptData)
                    const overallApptDepartmentsCount = Object.values(this.overallAppointmentsByDeptData)

                    this.overallAppointmentsByDeptChart = new Chart(ctx2, {
                        type: "pie",
                        data: {
                            labels: overallApptDepartments,
                            datasets: [{
                                label: "Appointments",
                                data: overallApptDepartmentsCount,
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
                    this.overallAppointmentsBydoctorsData = results.overall_appt_by_doctors
                    const ctx3 = document.getElementById('overallAppointmentsBydoctorsChart').getContext('2d')
                    const overallDoctorAppointments = Object.keys(this.overallAppointmentsBydoctorsData)
                    const overallDoctorAppointmentsCount = Object.values(this.overallAppointmentsBydoctorsData)

                    this.overallAppointmentsBydoctorsChart = new Chart(ctx3, {
                        type: "pie",
                        data: {
                            labels: overallDoctorAppointments,
                            datasets: [{
                                label: "Doctors",
                                data: overallDoctorAppointmentsCount,
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
                    this.thisMonthAppointmentsByDeptData = results.this_month_appt_by_dept
                    const ctx4 = document.getElementById('thisMonthAppointmentsByDeptChart').getContext('2d')
                    const thisMonthApptDepartments = Object.keys(this.thisMonthAppointmentsByDeptData)
                    const thisMonthApptDepartmentsCount = Object.values(this.thisMonthAppointmentsByDeptData)

                    this.overallAppointmentsByDeptChart = new Chart(ctx4, {
                        type: "pie",
                        data: {
                            labels: thisMonthApptDepartments,
                            datasets: [{
                                label: "Appointments",
                                data: thisMonthApptDepartmentsCount,
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

                    // Chart 5
                    this.thisMonthAppointmentsBydoctorsData = results.this_month_appt_by_doctors
                    const ctx5 = document.getElementById('thisMonthAppointmentsBydoctorsChart').getContext('2d')
                    const thisMonthApptDoctors = Object.keys(this.thisMonthAppointmentsBydoctorsData)
                    const thisMonthApptDoctorsCount = Object.values(this.thisMonthAppointmentsBydoctorsData)

                    this.overallAppointmentsByDeptChart = new Chart(ctx5, {
                        type: "pie",
                        data: {
                            labels: thisMonthApptDoctors,
                            datasets: [{
                                label: "Appointments",
                                data: thisMonthApptDoctorsCount,
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