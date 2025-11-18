from rest_framework import viewsets, generics
from .models import BasicVitals, Consultation, PrescriptionItem, LabTestOrder
from .serializers import (
    BasicVitalsSerializer, 
    ConsultationSerializer, 
    PrescriptionItemSerializer, 
    LabTestOrderSerializer,
    PatientHistorySerializer # <-- UN-COMMENTED
)
# --- This is the main change ---
# We import our new custom permission
from clinic_admin.permissions import IsDoctor
# ------------------------------

# --- Add these imports ---
import datetime
from receptionist.models import Appointment, Patient     # <-- UN-COMMENTED
# from receptionist.serializers import AppointmentSerializer  # <-- UN-COMMENTED
# -------------------------


# class MyTodayAppointmentsViewSet(viewsets.ReadOnlyModelViewSet): # <-- UN-COMMENTED CLASS
#     """
#     A 'read-only' view that shows the logged-in doctor
#     THEIR appointments scheduled for TODAY.
#     """
#     # --- PERMISSION UPDATED ---
#     permission_classes = [IsDoctor]
#     serializer_class = AppointmentSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         today = datetime.date.today()
        
#         if not hasattr(user, 'staff') or not hasattr(user.staff, 'doctor'):
#              return Appointment.objects.none()

#         return Appointment.objects.filter(
#             doctor=user.staff.doctor, 
#             appointment_date__date=today
#         ).order_by('appointment_date')


class PatientHistoryView(generics.RetrieveAPIView): # <-- UN-COMMENTED CLASS
    """
    A 'read-only' view that gets a single Patient by their ID
    and returns their *complete* medical history.
    """
    # --- PERMISSION UPDATED ---
    permission_classes = [IsDoctor]
    queryset = Patient.objects.all()
    serializer_class = PatientHistorySerializer
    lookup_field = 'id' 


# --- All ViewSets below are now locked to Doctors only ---

class BasicVitalsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = BasicVitals.objects.all()
    serializer_class = BasicVitalsSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer

class LabTestOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    queryset = LabTestOrder.objects.all()
    serializer_class = LabTestOrderSerializer