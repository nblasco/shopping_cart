from enum import Enum

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Item(models.Model):
    """ Item represents each course or other product of the cart """

    class Category(Enum):
        """ This class represents the different categories of courses """

        animation = ('an', 'Animación')
        design = ('des', 'Diseño')
        web_design = ('wdes', 'Diseño Web')
        photography = ('phot', 'Fotografía')
        unity = ('un', 'Unity')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    class Level(Enum):
        """ This class represents the level of the course """

        basic = ('b', 'Curso Básico')
        avanced = ('a', 'Curso Avanzado')
        complete = ('c', 'Curso Completo')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    name = models.CharField(max_length=300, verbose_name='Item')
    category = models.CharField(max_length=200,
                                choices=[x.value for x in Category],
                                verbose_name='Category')
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                verbose_name='Price')
    level = models.CharField(max_length=150, choices=[x.value for x in Level],
                             verbose_name='Level')
    date_created = models.DateTimeField(default=timezone.now)
    image = models.FileField(upload_to='items/', blank=True, null=True)

    class Meta:
        ordering = ['name', 'date_created']
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return 'Item %s - %s' % (self.name, self.price)

    def __unicode__(self):
        return u'Item %s - %s' % (self.name, self.price)


class Cart(models.Model):
    """ This model represents the shopping cart """

    user = models.ForeignKey(User, verbose_name='User')
    items = models.ManyToManyField(Item, verbose_name='Items')
    total = models.DecimalField(blank=True, default=0, max_digits=8,
                                decimal_places=2, verbose_name='Total')
    date_created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user', 'date_created']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return 'Cart %s - %s' % (self.id, self.user.username)

    def __unicode__(self):
        return u'Cart %s - %s' % (self.id, self.user.username)

    def set_total(self):
        """ This method calculates the total of the shopping cart """

        self.total = 0
        for item in self.items.all():
            self.total += item.price
        self.save()
