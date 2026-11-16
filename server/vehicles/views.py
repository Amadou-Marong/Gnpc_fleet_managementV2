from rest_framework import generics
from .serializers import ( 
    VehicleSerializer, 
    VehicleRequestSerializer,
    VehicleRequestStatusSerializer,
    VehicleRequestAssignSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions import IsAdminOrCreateReadOnly
from .models import Vehicle, VehicleRequest
# Create your views here.

class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCreateReadOnly]
    

class VehicleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCreateReadOnly]

    def get_permissions(self):
        # Require admin rights for updating or deleting
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        
        # Allow anyone to view (GET, HEAD, OPTIONS)
        return [AllowAny()]
    

class VehicleRequestListCreateView(generics.ListCreateAPIView):
    queryset = VehicleRequest.objects.all()
    serializer_class = VehicleRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCreateReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        

class VehicleRequestActionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleRequest.objects.all()
    serializer_class = VehicleRequestSerializer
    
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            if 'assigned_vehicle' in self.request.data or 'assigned_driver' in self.request.data:
                return VehicleRequestAssignSerializer
            return VehicleRequestStatusSerializer
        return VehicleRequestSerializer
    
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminUser()]
        return[IsAuthenticated()]
    
