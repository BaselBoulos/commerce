from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User
from .forms import *
from .models import AuctionListing, WishList
from django.http import Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = 'auctions/index.html'
    context_object_name = 'all_listings'

    def get_queryset(self):
        return AuctionListing.objects.all()


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    listingform = AuctionListingForm
    if request.method == "POST":
        listingform = AuctionListingForm(request.POST)
        if listingform.is_valid():
            listingform = listingform.save()
            listingform.seller = request.user.username
            listingform.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/new_listing.html", {
        "listingform": listingform,
    })


class DetailView(generic.DetailView):
    model = AuctionListing
    context_object_name = 'listing'
    template_name = "auctions/listing_details.html"


class ListingDelete(generic.DeleteView):
    model = AuctionListing
    success_url = reverse_lazy('index')


def add_to_wishlist(request, product_id):
    product = WishList.objects.filter(listing_id=product_id, user=request.user.username)
    if product:
        product.delete()
        messages.success(request, "Removed From ")
    else:
        product = WishList()
        product.listing_id = product_id
        product.user = request.user.username
        product.save()
        messages.success(request, "Added To ")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def wishlist(request):
    product = WishList.objects.filter(user=request.user)
    listing_ids = WishList.objects.values_list('listing_id', flat=True)
    listings = AuctionListing.objects.filter(pk__in=listing_ids)
    return render(request, "auctions/wishlist.html", {
        'wishlist': product,
        'listings': listings
    })


