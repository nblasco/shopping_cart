from django.shortcuts import render
from django.views.generic import ListView

from .models import Item, Cart


class ItemListView(ListView):
    """ ItemListView is responsible for showing all available courses """

    model = Item
    queryset = Item.objects.all().order_by('name')[:10]