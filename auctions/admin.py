from django.contrib import admin
from .models import Listing, Watchlist

class WatchlistAdmin(admin.ModelAdmin):
   filter_horizontal = ()

# Register your models here.
admin.site.register(Listing)
admin.site.register(Watchlist, WatchlistAdmin)