from django.urls import path
from .views import (
    VehicleListCreateView,
    VehicleRetrieveUpdateDestroyView,
    VehicleRequestListCreateView,
    VehicleRequestActionView,
    DispatchDataView
)

urlpatterns = [
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicles'),
    path('vehicles/<int:pk>/', VehicleRetrieveUpdateDestroyView.as_view(), name='vehicle-retrieve-update-destroy'),
    
    path('vehicles/requests/', VehicleRequestListCreateView.as_view(), name='requests'),
    
    path('vehicles/requests/<int:pk>/', VehicleRequestActionView.as_view(), name='vehicle-request-detail'),
    
    path('vehicles/dispatch-data/', DispatchDataView.as_view(), name='dispatch-data')
]