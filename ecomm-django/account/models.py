from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    user_name = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    town = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Addresses'
