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


def cart_detail(request):
    """ This view show all items from chopping cart 

    Show the courses added to the cart regardless of whether the user
    is logged in or is anonymous
    :param request: 
    :return: HttpResponse
    """

    if request.user.is_anonymous:
        items = []
        total = 0
        if 'cart' in request.session:
            data = json.loads(request.session['cart'])
            for item_id in data['items']:
                item = Item.objects.get(pk=item_id)
                items.append(item)
                total += item.price
        return render(request, 'cart/cart_detail.html',
                      {'items': items, 'total': total})
    else:
        try:
            cart = Cart.objects.get(user=request.user, active=True)
        except Cart.DoesNotExist:
            return render(request, 'cart/cart_detail.html',
                          {'items': [], 'total': 0})

        items = cart.items.all()
        total = cart.total
        return render(request, 'cart/cart_detail.html',
                      {'items': items, 'total': total})


def pay_shopping_cart(request):
    """ Preview the payment of the shopping cart

    if the user is not logged in, it redirects to login.
    :param request: 
    :return: HttpResponse
    """

    if request.user.is_anonymous:
        request.session['pay'] = True
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        try:
            cart = Cart.objects.get(user=request.user, active=True)
        except Cart.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('item_list'))

        return render(request, 'cart/cart_payment.html', {'cart': cart})
