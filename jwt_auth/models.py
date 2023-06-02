from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  email = models.CharField(max_length=100, unique=True)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)