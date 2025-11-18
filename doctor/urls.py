from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BasicVitalsViewSet, 
    ConsultationViewSet, 
    PrescriptionItemViewSet, 
    LabTestOrderViewSet,
   # MyTodayAppointmentsViewSet,  # <-- UN-COMMENTED
    PatientHistoryView         # <-- UN-COMMENTED
)

# The router automatically creates the URLs for our ViewSets
router = DefaultRouter()
router.register(r'basic-vitals', BasicVitalsViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'prescription-items', PrescriptionItemViewSet)
router.register(r'lab-test-orders', LabTestOrderViewSet)
#router.register(r'my-today-appointments', MyTodayAppointmentsViewSet, basename='my-today-appointments') # <-- UN-COMMENTED

# This is the main variable this file exports
urlpatterns = [
    # All the router URLs are included here
    path('', include(router.urls)),
    
    # --- ADD THIS NEW MANUAL URL ---
    # This creates a URL like: api/doctor/patient-history/123/
    path(
        'patient-history/<int:id>/', 
        PatientHistoryView.as_view(), 
        name='patient-history'
    ),
]