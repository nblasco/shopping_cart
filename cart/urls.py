from django.conf.urls import url

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
]
