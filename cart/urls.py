from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ItemListView.as_view(),
        name='item_list'
    ),

]
