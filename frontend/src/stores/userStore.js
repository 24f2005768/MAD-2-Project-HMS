import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { requestAPI } from '../../utils/api';

export const useUserStore = defineStore('userStore', {
  
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: (() => {
      try {
        const data = localStorage.getItem('user');
        return data ? JSON.parse(data) : null;
      }

      catch (error) {
        console.log('Could not get user', error);
        return null
      }
    })()
  }),

  getters: {
    isAuthenticated: (state) => state.token ? true : false,
    role: (state) => state.user ? state.user.role : null,
    doctorId: (state) => state.user && state.user.doctor_id ? state.user.doctor_id : null,
    patientId: (state) => state.user && state.user.patient_id ? state.user.patient_id : null
  },

  actions: {
    async login(data) {
      const request = await requestAPI('POST', data, '/login')

      const token = request['token']
      const user = {
        "user_id": request['user_id'],
        "user_name": request['user_name'],
        "contact_number": request['contact_number'],
        "email": request['email'],
        "role": request['role'],
      }

      // Add role-specific IDs 
      if (request['doctor_id']) {
        user.doctor_id = request['doctor_id'];
      }
      if (request['patient_id']) {
        user.patient_id = request['patient_id'];
      }
      if (request['admin_id']) {
        user.admin_id = request['admin_id'];
      }

      this.token = token
      this.user = user

      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)

      return user
    },

    logout() {
      this.token = null
      this.user = null 

      localStorage.removeItem('user')
      localStorage.removeItem('token')
    }
  }
})

