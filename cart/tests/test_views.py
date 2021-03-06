# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware

from cart.models import Item, Cart
from cart.views import add_item_cart, delete_item_cart


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_response(request)
    return request

class ItemTest(TestCase):
    """ Test items to cart
    
    1.- Item list
    2.- Add item to cart with user Login
         2.1.- Empty cart
         2.2.- You already have items in the cart, and the current one is not
         2.3.- Try adding an item that is already in the cart
    3.- Add item to cart with user anonymous
         3.1.- Empty cart
         3.2.- You already have items in the cart, and the current one is not
         3.3.- Try adding an item that is already in the cart
    4.- Item delete
    """

    fixtures = ['cart/fixtures/item.json', 'cart/fixtures/user.json', ]

    def setUp(self):
        self.user = User.objects.get(id=2)
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)

        self.factory = RequestFactory()

    def test_item_list(self):
        """ Test view of item list """

        url = reverse('item_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.context['item_list']), 4)

    def test_user_add_item_cart_empty(self):
        """ Add items to cart - 2.1 

        2.- User Login
            2.1.- Empty cart
        """

        request = self.factory.get(reverse('item_add', kwargs={'item_id': '1'}))
        request.user = self.user

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = add_item_cart(request, 1)

        cart = Cart.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.item1 in cart.items.all())

    def test_user_add_item_cart(self):
        """ Add items to cart - 2.2 

        2.- User Login
            2.2.- You already have items in the cart, and the current one is not
        """

        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.add(self.item2)
        self.cart.save()

        request = self.factory.get(reverse('item_add', kwargs={'item_id': '1'}))
        request.user = self.user

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = add_item_cart(request, 1)
        cart = Cart.objects.get(id=1)

        self.assertTrue(self.item1 in cart.items.all())
        self.assertEqual(response.status_code, 200)

    def test_user_add_item_cart(self):
        """ Add items to cart - 2.3 

        2.- User Login
            2.3.- Try adding an item that is already in the cart
        """

        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.add(self.item1)
        self.cart.save()

        request = self.factory.get(reverse('item_add', kwargs={'item_id': '1'}))
        request.user = self.user

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = add_item_cart(request, 1)
        cart = Cart.objects.get(id=1)

        self.assertTrue(cart.items.count() == 1)
        self.assertTrue(self.item1 in cart.items.all())
        self.assertEqual(response.status_code, 200)

    def test_anonymous_add_item_cart_empty(self):
        """ Add items to cart - 3.1   

        3.- User anonymous
            3.1.- Empty cart
        """

        self.client.get(reverse('item_add', kwargs={'item_id': '1'}))
        count_items = self.client.session['count_items']

        self.assertEqual(count_items, 1)

    def test_anonymous_add_item_cart(self):
        """ Add items to cart - 3.2   

        3.- User anonymous
            3.2.- You already have items in the cart, and the current one is not
        """

        session = self.client.session
        session['count_items'] = 1
        session['cart'] = '{"items":[1]}'
        session.save()

        self.client.get(reverse('item_add', kwargs={'item_id': '2'}))
        count_items = self.client.session['count_items']

        self.assertEqual(count_items, 2)

    def test_anonymous_add_item_exist_cart(self):
        """ Add items to cart - 3.3   

        3.- User anonymous
            3.3.- Try adding an item that is already in the cart
        """

        session = self.client.session
        session['count_items'] = 1
        session['cart'] = '{"items":[1]}'
        session.save()

        self.client.get(reverse('item_add', kwargs={'item_id': '1'}))
        count_items = self.client.session['count_items']

        self.assertEqual(count_items, 1)

    def test_anonymous_cart_remove_item(self):
        """ Test view remove item of cart with user anonymous """

        url = reverse('cart_remove_item', kwargs={'item_id':1})

        session = self.client.session
        session['count_items'] = 1
        session['cart'] = '{"items":[1,2]}'
        session.save()
        response = self.client.get(url)

        self.assertEqual(len(response.context['items']), 1)

    def test_user_cart_remove_item(self):
        """ Test view remove item of cart with user login """

        url = reverse('cart_remove_item', kwargs={'item_id': 1})

        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.add(self.item1)
        self.cart.items.add(self.item2)
        self.cart.save()

        request = self.factory.get(url)
        request.user = self.user

        request = add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = delete_item_cart(request, 1)
        cart = Cart.objects.get(id=1)

        self.assertTrue(cart.items.count() == 1)
        self.assertTrue(not self.item1 in cart.items.all())


class CartDetailTest(TestCase):
    """ Test view of detail cart """

    fixtures = ['cart/fixtures/item.json', 'cart/fixtures/user.json', ]

    def setUp(self):
        """ Set values default for test """

        self.item = Item.objects.get(id=1)
        self.user = User.objects.get(id=2)

        self.factory = RequestFactory()

    def test_anonymous_cart_detail(self):
        """ Test view cart detail when user is anonymous """

        session = self.client.session
        session['count_items'] = 1
        session['cart'] = '{"items":[1]}'
        session.save()

        response = self.client.get(reverse('cart_detail'))

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['total'], self.item.price)

    def test_user_cart_detail(self):
        """ Test view cart detail when user is login """

        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.add(self.item)
        self.cart.set_total()
        self.cart.save()
        self.client.login(username='norma', password='n_123456')

        response = self.client.get(reverse('cart_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['total'], self.item.price)