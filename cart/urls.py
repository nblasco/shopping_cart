from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ItemListView.as_view(),
        name='item_list'
    ),
    url(
        regex=r'^add/(?P<item_id>\d+)/$',
        view=views.add_item_cart,
        name='item_add'
    ),
    url(
        regex=r'^cart/$',
        view=views.cart_detail,
        name='cart_detail'
    ),
    url(
        regex=r'^login/$',
        view=auth_views.LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^logout/$',
        view=auth_views.LogoutView.as_view(),
        name='logout'
    ),
]
