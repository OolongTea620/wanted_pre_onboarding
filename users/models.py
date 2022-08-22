from django.db import models
from bases.models import Base
from postings.models import Posting

class User(Base):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    posting = models.ForeignKey(Posting, on_delete = models.SET_NULL, null=True, default = None)