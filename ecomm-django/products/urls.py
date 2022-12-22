from django.urls import path
from .views import *


app_name ='products'


urlpatterns = [
    path('', new_arrival, name='new_arrival'),
    path('products_page/', products_home, name='products_page'),
    path('product-detail/<int:id>', product_detail, name='product_detail'),
    path('add-to-cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>', remove_from_cart, name='remove_from_cart'),
]
