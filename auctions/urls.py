from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createListing"),
    path("listingDetails/<str:listing_id>", views.listing_details, name="listingDetails"),
     path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="addWatchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="removeWatchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
]
