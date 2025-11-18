from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicineViewSet, 
    PharmacyBillViewSet, 
    PendingPrescriptionViewSet # <-- Add this
)

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'bills', PharmacyBillViewSet)
router.register(r'pending-prescriptions', PendingPrescriptionViewSet, basename='pending-prescriptions') # <-- Add this

urlpatterns = [
    path('', include(router.urls)),
]