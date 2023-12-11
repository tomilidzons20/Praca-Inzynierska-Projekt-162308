from rest_framework.generics import CreateAPIView

from .models import CarMaintenance
from .serializers import CarMaintenanceSerializer


class MaintenanceCreateAPIView(CreateAPIView):
    serializer_class = CarMaintenanceSerializer
    queryset = CarMaintenance
