from django.db import models
from company.models import Company

# Create your models here.
class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    minsalary = models.DecimalField(max_digits=10, decimal_places=2)
    maxsalary = models.DecimalField(max_digits=10, decimal_places=2)
    responsibilities = models.JSONField(default=list)
    requirements = models.JSONField(default=list)
    type = models.CharField(max_length=50)  # e.g., 'full-time', 'part-time', 'internship'
    experience_level = models.CharField(max_length=50)  # e.g., 'junior', 'mid', 'senior'
    posted_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100) # e.g., 'IT', 'Finance', 'Marketing'
    is_active = models.BooleanField(default=True)  # Permet de désactiver une offre sans la supprimer
    