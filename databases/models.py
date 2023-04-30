from django.db import models
from django.conf import settings

CONNECTION_CHOICES = [
        ('mysql', 'mysql'),
        ('oracle', 'oracle'),
        ('postgresql', 'postgresql'),
    ]
    
# Create your models here.
class Connection(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=CONNECTION_CHOICES)

    def __str__(self):
        return self.name
    
