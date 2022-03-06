from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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

def sell(request):
    form = SellForm()
    if request.method == "POST":
        form = SellForm(request.POST)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/sell.html", {
        "form": form,
    })

def listing(request, listing_id):
    form = CommentForm()
    comments = Comments.objects.filter(listing_id=listing_id)
    listing = Listing.objects.get(pk=listing_id)
    watch = Watchlist()
    highest = HighestBid()

    seller = False
    if request.user == listing.user:
        seller = True

    if request.method == "POST" and 'btnform1' in request.POST:
        listing.price = request.POST["bid"]
        listing.save()
        HighestBid.objects.filter(listing_id=listing_id).delete()
        highest.user = request.user
        highest.listing_id = listing_id
        highest.save()
        return HttpResponseRedirect(request.path_info)
    
    if request.method == "POST" and 'btnform2' in request.POST:
        watch.user = request.user
        watch.listing = listing
        watch.save()
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'btnform3' in request.POST:
        Watchlist.objects.filter(user_id=request.user,listing_id=listing_id).delete()

    if request.method == "POST" and 'btnform4' in request.POST:
        listing.active = False
        listing.save()

    if request.method == "POST" and 'btnform5' in request.POST:
        listing.delete()
        return HttpResponseRedirect(reverse("index")) 

    if request.method == "POST" and 'btnform6' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.user = request.user
            assign.listing_id = listing_id
            form.save()
            return HttpResponseRedirect(request.path_info)

    bool = False 
    try:
        for i in Watchlist.objects.filter(user_id=request.user):
            if listing_id == i.listing_id:
                bool=True
    except:
        pass
    
    try:
        checkuser = HighestBid.objects.filter(listing_id=listing_id, user_id=request.user).exists()
    except:
        checkuser = False

    highestbid = False
    if listing.active == False and checkuser == True:
        highestbid = True
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "minbid": (listing.price + 1),
        "watching": bool,
        "seller": seller,
        "form": form,
        "comments": comments,
        "active": listing.active,
        "winner": highestbid
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def catindex(request, cat_name):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=cat_name)
    })

def watchlist(request):
    watchlist = []
    for i in Watchlist.objects.filter(user_id=request.user):
        watchlist.append(Listing.objects.get(pk=i.listing_id))
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def yourlistings(request):
    return render(request, "auctions/yourlistings.html", {
        "listings": Listing.objects.filter(user_id=request.user)
    })