from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .forms import ListingForm, BidForm

from .models import User, Listing, Watchlist, Bid, ClosedListing

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


@login_required
def create_listing(request, user):
    if request.method == "POST":
        listingForm = ListingForm(request.POST,  request.FILES)

        if listingForm.is_valid():
            listingForm.instance.listed_by = request.user
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
    
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        listing_in_watchlist = watchlist.listings.get(id = listing_id)
        listing_in_watchlist = True
    except:
        listing_in_watchlist = False
    
    return render(request, "auctions/listing-details.html", {
        'listing': listing,
        'image': listing.image,
        'bidForm' : BidForm(),
        'listing_in_watchlist': listing_in_watchlist
    })

def watchlist(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {
            'watchlists': watchlist.listings.all()
        })
    except:
        return render(request, "auctions/watchlist.html", {
            'watchlists': False
        })

    return HttpResponseRedirect(reverse("auctions:index"))

    
def lastPK(obj):
    length = len(obj.objects.all())+1
    return length

def add_watchlist(request, listing_id):
    if Watchlist.objects.filter(user=request.user).exists():
        watchlist = Watchlist.objects.get(user=request.user)
    else:
        watchlist = Watchlist(id = lastPK(Watchlist),user = request.user)
        
    watchlist.save()
    listing = Listing.objects.get(id=listing_id)
    watchlist.listings.add(listing)
    watchlist.save()

    return render(request, "auctions/watchlist.html",{
        "watchlists" : watchlist.listings.all()
    })

def remove_watchlist(request, listing_id):
    watchlist = Watchlist.objects.get(user=request.user)
    listing = Listing.objects.get(id=listing_id)
    watchlist.listings.remove(listing)

    return render(request, "auctions/watchlist.html",{
        "watchlists" : watchlist.listings.all(),
        "remove_watchlist_message": "You have successfully removed item from watchlist!"
    })
    
@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.method == "POST":
        bidForm = BidForm(request.POST)

        if bidForm.is_valid():
            bidForm.instance.bided_by = request.user
            bidForm.instance.listings = listing
            bidForm = bidForm.save()

            starting_bid = listing.starting_bid

            if (bidForm.bid>starting_bid):
                listing.starting_bid = bidForm.bid
                Listing.objects.filter(pk=listing_id).update(starting_bid=bidForm.bid)
                successBidMessage = 'Congratulations! New Bid is added by '

                return render(request, 'auctions/listing-details.html', {
                    'successBidMessage': successBidMessage,
                    'bid' : bidForm,
                    'bidForm' : BidForm(),
                    'listing': listing,
                    'image': listing.image
                })
            else:
                failedBidMessage = 'Sorry! New bid have to be greater than the current bid!!!'
                return render(request, 'auctions/listing-details.html', {
                'failedBidMessage': failedBidMessage,
                'bidForm' : BidForm(),
                'listing': listing,
                'image': listing.image
            })
            
            

    return render(request, "auctions/listing-details.html", {
        'bidForm' : BidForm(),
        'listing': listing,
        'image': listing.image,
    })

# def close_listing(request, listing_id):
#     listing = Listing.objects.get(id=listing_id)
#     Listing.delete(listing)

#     return render(request, "auctions/index.html", {
#         'close_listing_message' : 'You have Successfully closed one of your Listings ',
#         'listing': listing,
#         'listings': Listing.objects.all()
#     })

@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    closed_listing_image = listing.image

    if Bid.objects.filter(listings=listing).exists():
        bid = Bid.objects.filter(listings=listing)
        auction_winner = bid.order_by('bided_by')[0]
        closedlisting = ClosedListing(id = lastPK(ClosedListing), closed_listing= listing, auction_winner= auction_winner)
        closedlisting.save()

        return render(request, 'auctions/index.html', {
            'close_listing_message' : 'You have Successfully closed one of your Listings ',
            'listing': listing,
            'listings': Listing.objects.all(),
            'closed_listing_image': closed_listing_image,
            'auction_winner': auction_winner,
            'closed_listings': ClosedListing.objects.all()    
        })
    
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })

    # else:
    #     closedlisting = ClosedListing(id = lastPK(ClosedListing), closed_listing= listing)

            # closedlistingform.instance.user = request.user
            # closedlistingform.instance.closed_listing = listing
            # if Bid.objects.filter(listings=listing).exists():
            #     bid = Bid.objects.filter(listings=listing)
            #     auction_winner = bid.bided_by
            #     closedlistingform.instance.auction_winner = auction_winner
            # else:
            #     closedlistingform.instance.auction_winner = None
            # closedlistingform = closedlistingform.save()





        # if listing.listed_by==request.user:
        #     if Bid.objects.filter(listings=listing).exists():
        #         bid = Bid.objects.filter(listings=listing)
        #         auction_winner = bid.bided_by
        #         close_listing = ClosedListing(user = request.user, closed_listing = listing, auction_winner = auction_winner)
        #         # close_listing.save()
        #     else:
        #         close_listing = ClosedListing(user = request.user, closed_listing = listing)
        #         # close_listing.save()
