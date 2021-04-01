from django.contrib import admin
from .models import Listing, Watchlist, Bid

class WatchlistAdmin(admin.ModelAdmin):
   filter_horizontal = ()

# Register your models here.
admin.site.register(Listing)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid)