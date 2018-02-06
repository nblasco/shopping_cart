from django.contrib import admin

from .models import Item, Cart


class ItemAdmin(admin.ModelAdmin):
    """ Custom Item inside admin"""

    list_display = ['id', 'name', 'price', 'image']
    ordering = ['id', 'date_created', 'name']

admin.site.register(Item, ItemAdmin)


class CartAdmin(admin.ModelAdmin):
    """ Custom Cart inside admin"""

    list_display = ['id', 'user', 'date_created', 'active']
    ordering = ['id', 'date_created', 'user']


admin.site.register(Cart, CartAdmin)
