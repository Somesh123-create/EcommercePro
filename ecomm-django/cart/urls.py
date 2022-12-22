from django.urls import path
from .views import *

app_name ='cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/', payment, name='payment'),
    path('payment-completed/', payment_completed, name='payment_completed'),
]
