from django.db import models

# Create your models here.
class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)  # e.g., 'IT', 'FIN', 'MKT'
    
    def __str__(self):
        return self.name
