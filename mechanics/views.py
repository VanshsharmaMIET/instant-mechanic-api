from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Mechanic, ServiceRequest
from .serializers import MechanicSerializer, ServiceRequestSerializer


class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def create(self, request, *args, **kwargs):
        mechanic_id = request.data.get('mechanic')
        if mechanic_id is None:
            return Response({"mechanic": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not Mechanic.objects.filter(id=mechanic_id).exists():
            return Response({"mechanic": "Mechanic with this ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)