from django.db import models
from bases.models import Base

class Company(Base):
    name = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)