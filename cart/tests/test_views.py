# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from cart.models import Item

class ItemTest(TestCase):
    """ Test items to cart
    
    1.- Item list
    """

    fixtures = ['cart/fixtures/item.json', 'cart/fixtures/user.json', ]

    def setUp(self):
        self.user = User.objects.get(id=2)
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)

    def test_item_list(self):
        """ Test view of item list """

        url = reverse('item_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.context['item_list']), 4)