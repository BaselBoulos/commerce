from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_bid = models.IntegerField(null=True)
    current_price = models.IntegerField(null=True)
    image = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=100)
    seller = models.CharField(max_length=100, default="Default_Value")
    is_closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=100, default="Default_Value")

    def __str__(self):
        return f"{self.title} listing | {self.seller}"


class WishList(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} put a bid in for {self.price}"