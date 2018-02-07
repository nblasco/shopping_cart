import json

from django.shortcuts import render
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

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


@login_required(login_url='/login/')
def pay_method_cart(request):
    """This view allows you to pay for the shopping cart

    Pay the cart through the selected method, in this case, only change the 
    status of the cart to not active.   
    :param request: 
    :return: HttpResponse
    """

    try:
        cart = Cart.objects.get(user=request.user, active=True)
    except Cart.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('item_list'))
    cart.active = False
    cart.save()

    if 'cart' in request.session:
        del request.session['cart']
    if 'count_items' in request.session:
        del request.session['count_items']

    return HttpResponseRedirect(reverse_lazy('item_list'))


@receiver(user_logged_in)
def post_login(user, request, **kwargs):
    """ View to create cart once logged

    Once the logged-in user signal is received, this view is responsible for
    seeing if it has a cart in the session, and converting it into an instance 
    of the database.
    :param user: 
    :param request: 
    :return: HttpResponse
    """
    if 'cart' in request.session:
        cart, created = Cart.objects.get_or_create(user=user, active=True)
        items_id = json.loads(request.session['cart'])
        for item_id in items_id['items']:
            item = Item.objects.get(id=item_id)
            cart.items.add(item)
        cart.set_total()
        cart.save()

        if 'cart' in request.session:
            del request.session['cart']
        if 'pay' in request.session:
            del request.session['pay']
        return render(request, 'cart/cart_payment.html', {'cart': cart})


@receiver(user_logged_out)
def post_logout(user, **kwargs):
    """ View to close cart once logged

    Once the user signal not logged in is received, this view is responsible 
    for closing a cart if it is active
    :param user: 
    :return: 
    """
    try:
        cart = Cart.objects.get(user=user, active=True)
        cart.active = False
        cart.save()
    except Cart.DoesNotExist:
        pass