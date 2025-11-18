from rest_framework import viewsets
from rest_framework import generics, filters
from .models import Medicine, PharmacyBill
from .serializers import MedicineSerializer, PharmacyBillSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    # enable searching
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name']


class PharmacyBillViewSet(viewsets.ModelViewSet):
    queryset = PharmacyBill.objects.all()
    serializer_class = PharmacyBillSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name']
