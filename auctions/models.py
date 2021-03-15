from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    # listed_by = models.CharField(max_length=50, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    starting_bid = models.FloatField(max_length=254)
    image = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Price: {self.starting_bid}, Image: {self.image}, Category: {self.category}"

# class WatchlistModel(models.Model):
#     uesrname = models.foreignkey(User,  on_delete=models.CASCADE, )