# In labtechnician/serializers.py

from rest_framework import serializers
from .models import (
    LabTestCategory, 
    LabTestParameter, 
    LabReport, 
    LabReportResult, 
    LabBill, 
    LabBillItem
)

# --- Serializers for "Child" models ---

class LabTestParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestParameter
        fields = ['id', 'parameter_key', 'label', 'normal_range']

class LabReportResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReportResult
        fields = ['id', 'parameter', 'value']

class LabBillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabBillItem
        fields = ['id', 'test', 'price']

# --- Serializers for "Parent" models ---
# These serializers will show their "children" nested inside them.

class LabTestCategorySerializer(serializers.ModelSerializer):
    # This will show all parameters for this test category
    parameters = LabTestParameterSerializer(many=True, read_only=True)
    
    class Meta:
        model = LabTestCategory
        fields = ['id', 'category_name', 'price', 'parameters']

class LabReportSerializer(serializers.ModelSerializer):
    # This will show all results for this lab report
    results = LabReportResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = LabReport
        fields = [
            'id', 
            'appointment', 
            'patient', 
            'category', 
            'report_date', 
            'remarks', 
            'sample_collected', 
            'results'
        ]

class LabBillSerializer(serializers.ModelSerializer):
    # This will show all items for this lab bill
    items = LabBillItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = LabBill
        fields = ['id', 'appointment', 'patient', 'bill_date', 'total_amount', 'items']