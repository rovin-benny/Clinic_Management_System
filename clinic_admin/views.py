# In clinic_admin/views.py

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .permissions import IsAdmin  # Use our new Admin permission
from .serializers import UserRegistrationSerializer, StaffDetailSerializer, DoctorDetailSerializer
from .models import Staff, Doctor

# --- Imports from other apps ---
# We need the models and serializers to re-use them
from receptionist.models import Patient
from labtechnician.models import LabTestCategory, LabTestParameter
from doctor.serializers import PatientHistorySerializer 
from labtechnician.serializers import LabTestCategorySerializer, LabTestParameterSerializer 


class UserRegistrationView(generics.CreateAPIView):
    """
    Endpoint for an Admin to create a new User, Staff, and (if applicable) Doctor.
    URL: /api/clinic_admin/register-user/
    """
    permission_classes = [IsAdmin]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": f"User '{user.username}' created successfully as a {request.data['role']}."},
            status=status.HTTP_201_CREATED
        )

class StaffViewSet(viewsets.ModelViewSet):
    """ Read-only endpoint for viewing all staff. """
    permission_classes = [IsAdmin]
    queryset = Staff.objects.all()
    serializer_class = StaffDetailSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """ Read-only endpoint for viewing all doctors. """
    permission_classes = [IsAdmin]
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer

class AdminPatientHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for admins to view all patient history.
    This fulfills "see all patient history" and "no delete/create patient".
    URL: /api/clinic_admin/patient-history/
    URL: /api/clinic_admin/patient-history/<id>/
    """
    permission_classes = [IsAdmin]
    queryset = Patient.objects.all()
    serializer_class = PatientHistorySerializer # Re-using the serializer from the doctor app

class AdminLabTestCategoryViewSet(viewsets.ModelViewSet):
    """
    Full endpoint for admins to manage Lab Tests (create, update price, etc.).
    URL: /api/clinic_admin/manage-lab-tests/
    """
    permission_classes = [IsAdmin]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer # Re-using from lab app

class AdminLabTestParameterViewSet(viewsets.ModelViewSet):
    """
    Full endpoint for admins to manage Lab Test Parameters.
    URL: /api/clinic_admin/manage-lab-parameters/
    """
    permission_classes = [IsAdmin]
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer # Re-using from lab app