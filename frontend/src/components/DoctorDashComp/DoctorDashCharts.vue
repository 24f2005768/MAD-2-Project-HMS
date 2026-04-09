<template>
    <div class = "d-flex flex-wrap justify-content-evenly align-items-center gap-5">
        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 text-center">
            <canvas id="appointmentsByMonthChart">
            </canvas>
            <h6>Month wise distribution of Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="thisMonthBusiestSlotsChart">
                </canvas>
            <!-- </div> -->
            <h6>Slot wise distribution of this Month's Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="overallBusiestSlotsChart">
                </canvas>
            <!-- </div> -->
            <h6>Slot wise distribution of all Appointments</h6>
        </div>

        <div class = "d-flex justify-content-center align-items-center flex-column gap-2 w-25 text-center">
            <!-- <div> -->
                <canvas id="PatientsGenderChart">
                </canvas>
            <!-- </div> -->
            <h6>Gender wise distribution of Patients</h6>
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

                overallBusiestSlotsData: null, 
                overallBusiestSlotsChart: null,

                PatientsGenderData: null, 
                PatientsGenderChart: null, 

                thisMonthBusiestSlotsData: null,
                thisMonthBusiestSlotsChart: null,
            }
        },
        emits: ["error"],
        methods: {
            async getCharts() {
                try {
                    const doctorID = this.store.user.doctor_id;
                    const results = await requestAPI("GET", null, `/doctor/charts/${doctorID}`)
                    
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
                    this.overallBusiestSlotsData = results.overall_busiest_slots
                    const ctx2 = document.getElementById('overallBusiestSlotsChart').getContext('2d')
                    const overallSlots = Object.keys(this.overallBusiestSlotsData)
                    const overallSlotsCount = Object.values(this.overallBusiestSlotsData)

                    this.overallBusiestSlotsChart = new Chart(ctx2, {
                        type: "pie",
                        data: {
                            labels: overallSlots,
                            datasets: [{
                                label: "Slots",
                                data: overallSlotsCount,
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
                    this.thisMonthBusiestSlotsData = results.this_month_busiest_slots
                    const ctx3 = document.getElementById('thisMonthBusiestSlotsChart').getContext('2d')
                    const thisMonthSlots = Object.keys(this.thisMonthBusiestSlotsData)
                    const thisMonthSlotsCount = Object.values(this.thisMonthBusiestSlotsData)

                    this.thisMonthBusiestSlotsChart = new Chart(ctx3, {
                        type: "pie",
                        data: {
                            labels: thisMonthSlots,
                            datasets: [{
                                label: "Slots",
                                data: thisMonthSlotsCount,
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
                    this.PatientsGenderData = results.patients_by_gender
                    const ctx4 = document.getElementById('PatientsGenderChart').getContext('2d')
                    const Gender = Object.keys(this.PatientsGenderData)
                    const GenderCount = Object.values(this.PatientsGenderData)

                    this.PatientsGenderChart = new Chart(ctx4, {
                        type: "pie",
                        data: {
                            labels: Gender,
                            datasets: [{
                                label: "Gender",
                                data: GenderCount,
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