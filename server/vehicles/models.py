from django.db import models
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

# Create your models here.
class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('out_of_service', 'Out of service'),
        ('maintenance', 'Maintenance'),
    )
    model_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')
    mileage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.model_name}"
    

class VehicleRequest(models.Model):
    DEPARTMENT_CHOICES = (
        ('operations', 'Operations'),
        ('it', 'IT'),
        ('hr', 'HR'),
        ('accounting', 'Accounting'),
        ('audit', 'Audit'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('assigned', 'Assigned'),
        ('rejected', 'Rejected'),
    )
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    purpose = models.TextField()
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True, related_name='trips')
    assigned_driver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_trips', limit_choices_to={'role': 'driver'})
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Vehicle Request"
        verbose_name_plural = "Vehicle Requests"
    
    def __str__(self):
        return f"{self.name} - {self.from_location} - {self.to_location}"