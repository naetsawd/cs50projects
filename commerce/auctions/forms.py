from django.forms import ModelForm
from django import forms
from auctions.models import *

choices = Category.objects.all().values_list("name", "name")

choice_list=[]
rating = [1,2,3,4,5]

for choice in choices:
    choice_list.append(choice)

class SellForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ("user",)
        fields = ["title", "image", "price", "desc", "category"]
        labels = {
            "image": "Image Url",
            "price": "Starting Bid",
            "desc": "Description",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "desc": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(choices = choice_list, attrs={"class": "form-control"})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        exclude = ("user","listing")
        fields = ["title", "body"]
    
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "required": False}),
            "body": forms.Textarea(attrs={"class": "form-control", "required": False})
        }