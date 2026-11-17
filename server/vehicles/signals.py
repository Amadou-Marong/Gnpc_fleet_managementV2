from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vehicle, VehicleRequest

@receiver(post_save, sender=Vehicle)
def sync_vehicle_request_on_vehicle_update(sender, instance, created, **kwargs):
    if created:
        return # Ignore newly created vehicles
    
    # Find the active request linked to this vehicle
    # Using related_name='trips' defined on VehicleRequest.assigned_vehicle
    active_requests = instance.trips.filter(status='assigned')
    
    for request in active_requests:
        # Scenario 1: Vehicle becomes available again (e.g., trip finished or driver unassigned)
        if instance.status == 'available':
            request.status = 'completed'
            request.assigned_vehicle = None
            request.assigned_driver = None
            request.save()
            
        # Scenario 2: Vehicle goes into maintenance or out of service mid-assignment
        elif instance.status in ['maintenance', 'out_of_service']:
            request.status = 'approved' # Revert to approved so another vehicle can be assigned
            request.assigned_vehicle = None
            request.assigned_driver = None
            request.save()
            
        # Scenario 3: The driver (assigned_to) on the Vehicle was changed directly
        elif instance.status == 'assigned_to' and instance.assigned_driver != instance.assigned_to:
            request.assigned_to = request.assigned_driver
            request.save()
