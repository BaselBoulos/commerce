from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting/", views.new_listing, name="new_listing"),
    path("listing/<pk>", views.DetailView.as_view(), name="listing_details"),
    path("listing/<pk>/delete/", views.ListingDelete.as_view(), name="listing_delete"),
    path("addtowishlist/<int:product_id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),

]
