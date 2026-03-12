from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., 'Job Seeker', 'Employer', 'Admin'
    code = models.CharField(max_length=20, unique=True)  # e.g., 'job_seeker', 'employer', 'admin'

    def __str__(self):
        return self.name