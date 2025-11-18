from rest_framework import serializers
from .models import BasicVitals, Consultation, PrescriptionItem, LabTestOrder
from labtechnician.models import LabReport, LabReportResult
from receptionist.models import Patient

# --- STANDARD SERIALIZERS ---

class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    class Meta:
        model = PrescriptionItem
        fields = ['medicine_name', 'dosage', 'frequency', 'duration']

class LabTestOrderSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.category_name', read_only=True)
    class Meta:
        model = LabTestOrder
        fields = ['id', 'test', 'test_name']

class BasicVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicVitals
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'appointment', 'vitals', 'symptoms', 'diagnosis', 'notes',
            'fulfill_pharmacy_internally', 'fulfill_lab_internally',
            'prescription_items', 'lab_test_orders'
        ]

# --- HISTORY SERIALIZERS (NO BILLING) ---

class LabReportResultHistorySerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source='parameter.label')
    normal_range = serializers.CharField(source='parameter.normal_range')
    class Meta:
        model = LabReportResult
        fields = ['parameter_name', 'value', 'normal_range']

class LabReportHistorySerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='category.category_name')
    results = LabReportResultHistorySerializer(many=True, read_only=True)
    class Meta:
        model = LabReport
        fields = ['id', 'test_name', 'report_date', 'remarks', 'results']

class ConsultationHistorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='appointment.doctor.staff.full_name', read_only=True)
    visit_date = serializers.DateTimeField(source='appointment.appointment_date', read_only=True)
    prescription_items = PrescriptionItemSerializer(many=True, read_only=True)
    lab_test_orders = LabTestOrderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'doctor_name', 'visit_date', 'symptoms', 
            'diagnosis', 'notes', 'prescription_items', 'lab_test_orders'
        ]

class PatientHistorySerializer(serializers.ModelSerializer):
    """
    DOCTOR VIEW: Shows Consultations and Lab Reports.
    DOES NOT SHOW BILLS.
    """
    # We use a method field to get consultations safely
    consultations = serializers.SerializerMethodField()
    lab_reports = LabReportHistorySerializer(many=True, read_only=True, source='labreport_set')
    
    class Meta:
        model = Patient
        fields = [
            'id', 'patient_name', 'age', 'gender', 'blood_group',
            'consultations', 'lab_reports' 
        ]

    def get_consultations(self, obj):
        # Find all consultations linked to appointments for THIS patient
        consults = Consultation.objects.filter(appointment__patient=obj).order_by('-id')
        return ConsultationHistorySerializer(consults, many=True).data