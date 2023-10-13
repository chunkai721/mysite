from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    line_id = models.CharField(max_length=255, unique=True, null=True, blank=True)