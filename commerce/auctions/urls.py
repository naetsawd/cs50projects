from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell", views.sell, name="sell"),
    path("categories", views.categories, name="categories"),
    path("yourlistings", views.yourlistings, name="yourlistings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<str:cat_name>", views.catindex, name="cat_name")
    
]
