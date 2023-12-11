from rest_framework.serializers import ModelSerializer

from .models import CarMaintenance


class CarMaintenanceSerializer(ModelSerializer):
    class Meta:
        model = CarMaintenance
        fields = '__all__'
