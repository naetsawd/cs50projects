from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    desc = models.TextField()
    price = models.IntegerField()
    image = models.CharField (max_length=2048, null=True)
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Listing number {self.id}: {self.title}"

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=64)
    body = models.TextField()

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment {self.id} on {self.listing} by {self.user}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class HighestBid(models.Model):
    listing = models.ForeignKey(Listing, primary_key=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
