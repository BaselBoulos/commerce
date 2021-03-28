from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_bid = models.IntegerField(null=True)
    image = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=100)
    seller = models.CharField(max_length=100, default="Default_Value")


class WishList(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()

