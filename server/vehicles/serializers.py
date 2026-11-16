from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vehicle, VehicleRequest
from accounts.serializers import UserSerializer
User = get_user_model()


class VehicleSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ('id','model_name', 'status', 'assigned_to', 'assigned_to_name', 'mileage')
        
    def get_assigned_to_name(self, obj):
        return obj.assigned_to.full_name if obj.assigned_to else "Unassigned"
    

class VehicleRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_vehicle_name = serializers.CharField(source='assigned_vehicle.model_name', read_only=True)
    assigned_driver_name = serializers.CharField(source='assigned_driver.full_name', read_only=True)
    
    class Meta:
        model = VehicleRequest
        fields = (
            'id', 
            'name', 
            'department', 
            'purpose', 
            'from_location', 
            'to_location', 
            'date',
            'status',
            'assigned_vehicle',
            'assigned_driver',
            'assigned_vehicle_name',
            'assigned_driver_name',
            'created_by' 
        )
    

class VehicleRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRequest
        fields = ['status']
        
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError('Invalid User Action')
    
        if self.instance and self.instance.status != 'pending':
            raise serializers.ValidationError(f'Cannot update a request that is already {self.instance.status}')

        return value
    
    def to_representation(self, instance):
        # Return the full VehicleRequest object after PATCH
        return VehicleRequestSerializer(instance, context=self.context).data


class VehicleRequestAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRequest
        fields = ('assigned_vehicle', 'assigned_driver')
    
    def validate(self, attrs):
        if self.instance.status not in ['approved', 'assigned']:
            raise serializers.ValidationError("Only approved or assigned requests can be updated.")
        
        if not attrs.get('assigned_vehicle') or not attrs.get('assigned_driver'):
            raise serializers.ValidationError("Both a vehicle and a driver are required.")
        
        return attrs
    
    def update(self, instance, validated_data):
        driver = validated_data['assigned_driver']
        vehicle = validated_data['assigned_vehicle']
        
        # If reassigning a different vehicle, free up the previous one
        if instance.assigned_vehicle and instance.assigned_vehicle != vehicle:
            old_vehicle = instance.assigned_vehicle
            old_vehicle.status = 'assigned'
            old_vehicle.assigned_to = None
            old_vehicle.save()
            
        # Update request status to 'assigned'
        instance.assigned_vehicle = vehicle
        instance.assigned_driver = driver
        instance.status = 'assigned'
        instance.save()
        
        # Update vehicle status and assigned user
        vehicle.status = 'in_use'
        vehicle.assigned_to = driver
        vehicle.save()
        
        return instance
    
    def to_representation(self, instance):
        return VehicleRequestSerializer(instance, context=self.context).data
        