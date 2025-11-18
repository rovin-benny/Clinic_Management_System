from rest_framework import viewsets,filters
from .models import Patient,Appointment,ConsultationBill
from .serializers import PatientSerializer,AppointmentSerializer,ConsultationBillSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("id")
    serializer_class = PatientSerializer

    # Enable search only for name and phone
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient_name', 'phone']

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-id')
    serializer_class = AppointmentSerializer

    # Search API
    filter_backends = [filters.SearchFilter]
    search_fields = ['token', 'patient__patient_name']

class ConsultationBillViewSet(viewsets.ModelViewSet):
    queryset = ConsultationBill.objects.all().order_by('-id')
    serializer_class = ConsultationBillSerializer

    # Enable searching
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name', 'appointment__token']