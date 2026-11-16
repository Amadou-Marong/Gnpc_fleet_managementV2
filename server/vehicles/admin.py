from django.contrib import admin
from .models import Vehicle, VehicleRequest
# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'status', 'assigned_to', 'mileage')

@admin.register(VehicleRequest)
class VehicleRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'from_location', 'to_location', 'date', 'status']