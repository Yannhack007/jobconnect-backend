from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, unique=True)
    logo_url = models.URLField(blank=True, null=True, unique=True)
    industry = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'IT', 'Finance', 'Marketing'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name