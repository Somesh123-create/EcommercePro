from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOOSE = (
    ('P', 'PayPal'),
)


class CheckOutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={'class': 'form-control',}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    apartment = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Appartment, suite, unit etc: (optional)'}))
    town = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    same_billing_addres = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option  = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOOSE)
