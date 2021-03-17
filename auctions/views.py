from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .forms import ListingForm

from .models import User, Listing, Watchlist

class CreateWatchlistForm(forms.Form):
    entryTitle = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': "Title of the entry's page"}))

def index(request):
    return render(request, 'auctions/index.html', {
        'listings': Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        listingForm = ListingForm(request.POST,  request.FILES)

        if listingForm.is_valid():
            listingForm = listingForm.save()
            return render(request, 'auctions/index.html', {
                'message': 'New Listing Is Created, and listed at the end of the list!!!',
                'listingForm': listingForm,
                'listings': Listing.objects.all()
            })

    return render(request, "auctions/create-listing.html", {
        'username' : User.username,
        'listingForm' : ListingForm()
    })

def listing_details(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing-details.html", {
        'listing': listing,
        'image': listing.image
    })

def watchlist(request):
    watchlist = Watchlist.objects.get(user = request.user)

    return render(request, "actions/watchlist", {
        'watchlistslistings': watchlist.listings.all()
    })

def add_watchlist(request, listing_id):
  

def remove_watchlist(request, listing_id):
    
