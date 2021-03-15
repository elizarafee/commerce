from django.forms import ModelForm
from .models import Listing

# Create the form class.
class ListingForm(ModelForm):
   class Meta:
       model = Listing
    #    form['listed_by'].widget.attrs['readonly'] = True
       fields = '__all__'