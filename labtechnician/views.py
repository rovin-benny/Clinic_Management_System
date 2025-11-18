from rest_framework import viewsets
# --- This is the main change ---
# We import our new custom permission
from clinic_admin.permissions import IsLabTechnician
# ------------------------------

from .models import (
    LabTestCategory, 
    LabTestParameter, 
    LabReport, 
    LabReportResult, 
    LabBill, 
    LabBillItem
)
from .serializers import (
    LabTestCategorySerializer, 
    LabTestParameterSerializer, 
    LabReportSerializer, 
    LabReportResultSerializer, 
    LabBillSerializer, 
    LabBillItemSerializer
)

# --- All ViewSets below are now locked to LabTechnicians only ---

class LabTestCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer

class LabTestParameterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer

class LabReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer

class LabReportResultViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabReportResult.objects.all()
    serializer_class = LabReportResultSerializer

class LabBillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer

class LabBillItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLabTechnician]
    queryset = LabBillItem.objects.all()
    serializer_class = LabBillItemSerializer