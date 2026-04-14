from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('TECHNICIAN', 'Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return self.username
class Ticket(models.Model):
    STATUS_CHOICES = (
    ('REPORTED', 'Reported'),
    ('CHECKED', 'Checked'),
    ('RESOLVED', 'Resolved'),
)

    computer_id = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.computer_id} - {self.status}"