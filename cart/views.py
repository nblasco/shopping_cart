import json

from django.shortcuts import render
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Item, Cart


class ItemListView(ListView):
    """ ItemListView is responsible for showing all available courses """

    model = Item
    queryset = Item.objects.all().order_by('name')[:10]


def add_item_cart(request, item_id):
    """ Add item to shopping cart 

    If you are an anonymous user, add the element to the session.
    If you are logged in, create or obtain a shopping cart and add the item.
    :param request: 
    :param item_id: 
    :return: HttpResponse
    """

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('item-list'))

    if request.user.is_anonymous:
        if 'cart' in request.session:
            data = json.loads(request.session['cart'])
            if item.id not in data['items']:
                data['items'].append(item.id)
                request.session['count_items'] = len(data['items'])
                request.session['cart'] = json.dumps(data)
        else:
            request.session['cart'] = json.dumps({'items': [item.id]})
            request.session['count_items'] = 1
    else:
        cart, created = Cart.objects.get_or_create(user=request.user,
                                                   active=True)

        if item not in cart.items.all():
            cart.items.add(item)
            cart.set_total()
            cart.save()
        request.session['count_items'] = cart.items.count()

    items = Item.objects.all()[:10]
    return render(request,
                  'cart/item_list.html',
                  {'info': True, 'item_list': items})
