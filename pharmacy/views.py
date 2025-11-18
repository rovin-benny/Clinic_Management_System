from rest_framework import viewsets, filters
from clinic_admin.permissions import IsPharmacist
from .models import Medicine, PharmacyBill
from .serializers import MedicineSerializer, PharmacyBillSerializer

# --- Import Doctor models for the workflow ---
from doctor.models import Consultation
from doctor.serializers import ConsultationSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    """
    Manage Inventory (Add/Edit/Delete medicines).
    Only Pharmacists can do this.
    """
    permission_classes = [IsPharmacist]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name']

class PendingPrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    WORKFLOW: Shows consultations where the doctor ordered medicines
    ('fulfill_pharmacy_internally'=True) but they haven't been billed yet.
    This is the Pharmacist's "To-Do List".
    """
    permission_classes = [IsPharmacist]
    serializer_class = ConsultationSerializer # Re-use the doctor's serializer to see the meds

    def get_queryset(self):
        # Logic: 
        # 1. Doctor said "Internal Pharmacy"
        # 2. Has prescription items
        # 3. NOT in PharmacyBill table yet (simplified check)
        
        # Get IDs of consultations that are already billed
        billed_ids = PharmacyBill.objects.values_list('consultation_id', flat=True)
        
        return Consultation.objects.filter(
            fulfill_pharmacy_internally=True,
            prescription_items__isnull=False
        ).exclude(id__in=billed_ids).distinct().order_by('-id')

class PharmacyBillViewSet(viewsets.ModelViewSet):
    """
    Generate Bills. 
    When a bill is created, it automatically subtracts stock (via Serializer).
    """
    permission_classes = [IsPharmacist]
    queryset = PharmacyBill.objects.all().order_by('-id')
    serializer_class = PharmacyBillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name']