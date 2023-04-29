from django.db import models

CONNECTION_CHOICES = [
        ('mysql', 'mysql'),
        ('oracle', 'oracle'),
        ('postgresql', 'postgresql'),
    ]
    
# Create your models here.
class Connection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=CONNECTION_CHOICES)
    properties = models.JSONField()

    def __str__(self):
        return self.name
    
