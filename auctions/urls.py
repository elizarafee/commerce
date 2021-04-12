from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:user>/create_listing", views.create_listing, name="create_listing"),
    path("listing_details/<str:listing_id>", views.listing_details, name="listing_details"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
]
