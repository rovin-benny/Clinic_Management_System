from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, PharmacyBillViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'bills', PharmacyBillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
