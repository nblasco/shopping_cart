# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from cart.models import Item, Cart


class ItemTest(TestCase):
    """ Test for objects Item """

    def test_item_create(self):
        """ Test create item to cart """

        item = Item.objects.create(
            name = 'Adobe Illustrator: Sé un experto en Ilustración Digital',
            category = 'Diseño',
            level = 'Curso avanzado',
            price=29,
            image='items/adobe_illustrator.png'
        )

        self.assertEqual(item.price, 29)
        self.assertEqual(item.id, 1)

    def test_item_delete(self):
        """ Test delete item """

        item = Item.objects.create(
            name='Adobe Illustrator: Sé un experto en Ilustración Digital',
            category='Diseño',
            level='Curso avanzado',
            price=29,
            image='items/adobe_illustrator.png'
        )

        item.delete()

        self.assertEqual(Item.objects.count(), 0 )
