from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class Listing(models.Model):
    listed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    starting_bid = models.FloatField(max_length=254)
    image = models.ImageField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Price: {self.starting_bid}, Image: {self.image}, Category: {self.category}"



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listings = models.ManyToManyField(Listing, blank=True, related_name="listings")
    
    def __str__(self):
        return f"{self.user}'s wachlist: {self.listings}"

class Bid(models.Model):
    bided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_to_bid")
    bid = models.FloatField(max_length=254)

    def __str__(self):
        return f"{self.bided_by} has added new bid {self.bid} on {self.listings}"

class ClosedListing(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    closed_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="closed_listing")
    auction_winner = models.ForeignKey(Bid, on_delete=models.CASCADE, default=None , related_name="auction_winner")
    
    def __str__(self):
        return f"{self.user} has closed the listing - {self.closed_listing} & the auction winner is {self.auction_winner}"
