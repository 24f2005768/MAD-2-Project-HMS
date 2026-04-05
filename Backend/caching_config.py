from flask_caching import Cache

cache = Cache()

def invalidate_patient_caches(patient_id=None):
    from resources.patient_resources import PatientResources, AllPatientResources
            
    # Invalidate specific patient cache
    if patient_id:
        cache.delete_memoized(PatientResources.get, patient_id)
    
    # Invalidate all patients list
    cache.delete_memoized(AllPatientResources.get)
    
    # Invalidate search caches since patient data changed
    invalidate_search_caches()

def invalidate_doctor_caches(doctor_id=None):
    from resources.doctor_resources import (DoctorResources, AllDoctorResources, DoctorAppointments, Availability)
            
    # Invalidate specific doctor cache
    if doctor_id:
        cache.delete_memoized(DoctorResources.get, doctor_id)
        cache.delete_memoized(DoctorAppointments.get, doctor_id)
        cache.delete_memoized(Availability.get, doctor_id)
    
    # Invalidate all doctors list
    cache.delete_memoized(AllDoctorResources.get)
    
    # Invalidate search caches
    invalidate_search_caches()

def invalidate_department_caches(dept_id=None):
    from resources.department_resources import DepartmentResources, AllDepartmentResources
            
    # Invalidate specific department cache
    if dept_id:
        cache.delete_memoized(DepartmentResources.get, dept_id)
    
    # Invalidate all departments list
    cache.delete_memoized(AllDepartmentResources.get)
    
    # Invalidate search caches
    invalidate_search_caches()

def invalidate_appointment_caches(appointment_id=None, doctor_id=None, patient_id=None):
    from resources.appointment_resources import AppointmentResources, AllAppointmentResources
    from resources.doctor_resources import DoctorResources, DoctorAppointments
    from resources.patient_resources import PatientResources
            
    # Invalidate specific appointment cache
    if appointment_id:
        cache.delete_memoized(AppointmentResources.get, appointment_id)
    
    # Invalidate all appointments list
    cache.delete_memoized(AllAppointmentResources.get)
    
    # Invalidate related doctor and patient caches
    if doctor_id:
        cache.delete_memoized(DoctorResources.get, doctor_id)
        cache.delete_memoized(DoctorAppointments.get, doctor_id)
    
    if patient_id:
        cache.delete_memoized(PatientResources.get, patient_id)

def invalidate_search_caches():
    from resources.search_resources import AdminSearch, DoctorSearch, PatientSearch
            
    # Delete search caches
    cache.delete_memoized(AdminSearch.get)
    cache.delete_memoized(DoctorSearch.get)
    cache.delete_memoized(PatientSearch.get)

def invalidate_shift_caches(doctor_id=None, shift_id=None):
    from resources.appointment_resources import SelectShift
    from resources.doctor_resources import Availability, DoctorResources
    
    if shift_id and doctor_id:
        cache.delete_memoized(SelectShift.get, doctor_id, shift_id)
    
    if doctor_id:
        cache.delete_memoized(Availability.get, doctor_id)
        cache.delete_memoized(DoctorResources.get, doctor_id)
