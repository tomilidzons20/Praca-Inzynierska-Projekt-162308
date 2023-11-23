from rest_framework.generics import CreateAPIView

from .serializers import CarMaintenanceSerializer
from .models import CarMaintenance


class MaintenanceCreateAPIView(CreateAPIView):
    serializer_class = CarMaintenanceSerializer
    queryset = CarMaintenance
