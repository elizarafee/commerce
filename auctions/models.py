from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    starting_bid = models.FloatField(max_length=254)
    image = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Price: {self.starting_bid}, Category: {self.category}"
