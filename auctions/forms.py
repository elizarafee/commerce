from django.forms import ModelForm
from .models import Listing, Bid

# Create the form class.
class ListingForm(ModelForm):
   class Meta:
       model = Listing
       fields = '__all__'
       
class BidForm(ModelForm):
   class Meta:
       model = Bid
       fields = ['bid']
