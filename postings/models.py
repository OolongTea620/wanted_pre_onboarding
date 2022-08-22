from django.db import models
from bases.models import Base
from companies.models import Company

class Posting(Base):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=200)
    bounty = models.PositiveIntegerField()
    content = models.TextField()
    skill = models.CharField(max_length=120)