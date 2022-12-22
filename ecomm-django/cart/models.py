from django.db import models
from django.contrib.auth.models import User
from products.models import *
from account.models import Address
# Create your models here.



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.item)

    def get_toatl_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return str(self.user)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_toatl_item_price()
        return total
