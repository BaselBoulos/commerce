from django import forms
from .models import AuctionListing


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = [
            'title',
            'description',
            'start_bid',
            'image',
            'category',
        ]