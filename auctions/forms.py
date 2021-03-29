from django.forms import ModelForm
from .models import Listing, Bid

# Create the form class.
class ListingForm(ModelForm):
   class Meta:
       model = Listing
       fields = ['listed_by', 'title', 'description', 'starting_bid', 'image', 'category']
       
       
class BidForm(ModelForm):
   class Meta:
       model = Bid
       fields = ['bid']
