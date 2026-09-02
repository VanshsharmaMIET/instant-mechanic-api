from rest_framework import serializers
from .models import Mechanic, ServiceRequest


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = ['id', 'name', 'phone', 'location', 'rating', 'is_open', 'services']


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'customer_name', 'customer_phone', 'vehicle_number',
            'mechanic', 'service', 'problem_description', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        mechanic = data.get('mechanic')
        service = data.get('service')
        if mechanic and service and service not in mechanic.services:
            raise serializers.ValidationError({
                "service": f"'{service}' is not offered by {mechanic.name}. "
                           f"Available services: {mechanic.services}"
            })
        return data

    def create(self, validated_data):
        validated_data['status'] = 'PENDING'
        return super().create(validated_data)