# In clinic_admin/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Staff, Doctor, Department

# These are the roles the admin can create
ROLE_CHOICES = (
    ('Doctor', 'Doctor'),
    ('Receptionist', 'Receptionist'),
    ('LabTechnician', 'LabTechnician'),
    ('Pharmacist', 'Pharmacist'),
)

# In clinic_admin/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Staff, Doctor, Department

# --- Serializer for User Registration (This is the updated part) ---
ROLE_CHOICES = (
    ('Doctor', 'Doctor'),
    ('Receptionist', 'Receptionist'),
    ('LabTechnician', 'LabTechnician'),
    ('Pharmacist', 'Pharmacist'),
)

class UserRegistrationSerializer(serializers.Serializer):
    """
    Special serializer to create a new User, Staff, 
    and (if needed) Doctor, all at once.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    
    # Staff fields
    full_name = serializers.CharField()
    gender = serializers.CharField()
    joining_date = serializers.DateField()
    mobile_number = serializers.CharField()
    
    # Doctor fields (optional)
    consultation_fee = serializers.IntegerField(required=False, allow_null=True)
    designation = serializers.CharField(required=False, allow_null=True, max_length=20)
    availability = serializers.CharField(required=False, allow_null=True, max_length=30) # <-- FIELD ADDED
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        required=False, 
        allow_null=True
    )

    def validate(self, data):
        """
        Check that doctor fields are present if role is 'Doctor'.
        Check that username is unique.
        """
        if data['role'] == 'Doctor':
            # --- VALIDATION UPDATED ---
            if (not data.get('consultation_fee') or 
                not data.get('designation') or 
                not data.get('department') or
                not data.get('availability')): # <-- FIELD ADDED
                raise serializers.ValidationError(
                    "Doctor role requires consultation_fee, designation, availability, and department."
                )
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return data

    def create(self, validated_data):
        # 1. Create the User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        # 2. Add User to Group
        role_name = validated_data['role']
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)
        
        # 3. Create the Staff profile
        staff = Staff.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            gender=validated_data['gender'],
            joining_date=validated_data['joining_date'],
            mobile_number=validated_data['mobile_number']
        )
        
        # 4. Create Doctor profile if applicable
        if role_name == 'Doctor':
            Doctor.objects.create(
                staff=staff,
                consultation_fee=validated_data['consultation_fee'],
                designation=validated_data['designation'],
                department=validated_data['department'],
                availability=validated_data['availability'] # <-- FIELD ADDED
            )
        
        return user # Return the created user

# --- All other serializers (DepartmentSerializer, StaffSerializer, DoctorSerializer) stay the same ---

class StaffDetailSerializer(serializers.ModelSerializer):
    """ Serializer for viewing Staff details """
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.groups.first.name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['id', 'full_name', 'username', 'role', 'mobile_number', 'joining_date']

class DoctorDetailSerializer(serializers.ModelSerializer):
    """ Serializer for viewing Doctor details """
    staff = StaffDetailSerializer(read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'staff', 'consultation_fee', 'designation', 'availability', 'department_name']