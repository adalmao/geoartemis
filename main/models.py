from django.db import models


class Subscribe(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.CharField(max_length=255, null=False, blank=False)
    have_inscription = models.BooleanField(null=False,default=False)
