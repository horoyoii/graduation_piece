from django.db import models

# Create your models here.
class Device_profile(models.Model):
    device_profile_file = models.FileField(blank=True, null=True)