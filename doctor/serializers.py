from rest_framework import serializers
from .models import BasicVitals, Consultation, PrescriptionItem, LabTestOrder

# --- Add these imports ---
from labtechnician.models import LabReport, LabReportResult
from receptionist.models import Patient
# -------------------------

# This serializer will be "nested" inside the Consultation
class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ['medicine', 'dosage', 'frequency', 'duration']

# This serializer will also be "nested"
class LabTestOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestOrder
        fields = ['test']

class BasicVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicVitals
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    # These "nested" serializers will show the full prescription
    # and lab orders inside the consultation, which is very useful.
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 
            'appointment', 
            'vitals', 
            'symptoms', 
            'diagnosis', 
            'notes',
            'fulfill_pharmacy_internally', 
            'fulfill_lab_internally',
            'prescription_items',  # This will show the list of prescriptions
            'lab_test_orders'      # This will show the list of lab tests
        ]

# --- ADD THESE NEW SERIALIZERS FOR HISTORY ---

class LabReportResultHistorySerializer(serializers.ModelSerializer):
    """Shows a single line item from a lab report"""
    parameter_name = serializers.CharField(source='parameter.label')
    normal_range = serializers.CharField(source='parameter.normal_range')
    class Meta:
        model = LabReportResult
        fields = ['parameter_name', 'value', 'normal_range']

class LabReportHistorySerializer(serializers.ModelSerializer):
    """Shows a full lab report, including all its results"""
    test_name = serializers.CharField(source='category.category_name')
    results = LabReportResultHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = LabReport
        fields = ['id', 'test_name', 'report_date', 'remarks', 'results']

class ConsultationHistorySerializer(serializers.ModelSerializer):
    """Shows a full consultation, including prescriptions and lab orders"""
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Consultation
        fields = [
            'id', 
            'appointment', 
            'symptoms', 
            'diagnosis', 
            'notes', 
            'prescription_items', 
            'lab_test_orders'
        ]

class PatientHistorySerializer(serializers.ModelSerializer):
    """
    Shows *everything* for a patient.
    This is the "Top Level" serializer.
    """
    # Use 'source' to find related models. This looks for
    # 'consultation' on the 'appointment_set' and all 'labreport_set'
    consultations = ConsultationHistorySerializer(many=True, read_only=True, source='appointment_set.consultation')
    lab_reports = LabReportHistorySerializer(many=True, read_only=True, source='labreport_set')
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_name',
            'age',
            'gender',
            'blood_group',
            'consultations',
            'lab_reports'
        ]