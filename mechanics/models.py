from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Phone number must be a valid 10-digit Indian number starting with 6-9."
)

vehicle_validator = RegexValidator(
    regex=r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$',
    message="Enter a valid vehicle number, e.g. UP16AB1234."
)


class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    location = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    is_open = models.BooleanField(default=True)
    services = models.JSONField(
        default=list,
        help_text='List of services, e.g. ["Oil Change", "Tyre Repair"]'
    )

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=10, validators=[phone_validator])
    vehicle_number = models.CharField(max_length=15, validators=[vehicle_validator])
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='service_requests')
    service = models.CharField(max_length=100)
    problem_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service} ({self.status})"