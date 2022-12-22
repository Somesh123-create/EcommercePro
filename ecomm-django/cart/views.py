from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import View
from .forms import CheckOutForm
from django.contrib import messages
from account.models import Address
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def cart(request):
    try:
        order = get_object_or_404(Order, user=request.user, ordered=False)
        order_items = order.items.all()

        if request.method == 'POST':
            order_item_id = request.POST['order_item_id']
            order_item_quntity = request.POST['quantity']
            update_qty = get_object_or_404(OrderItem, id=order_item_id)
            update_qty.quantity = int(order_item_quntity)
            update_qty.save()

        context = {
            'order_items':order_items,
            'order':order,
        }
        return render(request, 'cart/cart.html', context)
    except :
        return render(request, 'cart/cart.html')
    return render(request, 'cart/cart.html', context)



class CheckOutView(View):
    def get(self, *args, **kwargs):
        try:
            order = get_object_or_404(Order, user=self.request.user, ordered=False)
            form = CheckOutForm()
            context = {
                'form':form,
                'order':order,
            }
            return render(self.request, 'cart/checkout.html', context)
        except:
            return redirect('cart:cart')

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                street = form.cleaned_data.get('street')
                apartment = form.cleaned_data.get('apartment')
                town = form.cleaned_data.get('town')
                email = form.cleaned_data.get('email')
                same_billing_addres = form.cleaned_data.get('same_billing_addres')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_addres = Address(
                    user = self.request.user,
                    first_name = first_name,
                    last_name = last_name,
                    phone = phone,
                    street_address = street,
                    apartment_address = apartment,
                    town = town,
                    email = email,
                    country = country,
                    zip = zip,
                    address_type = 'B',

                )
                billing_addres.save()
                order.billing_address = billing_addres
                order.save()
                return redirect('cart:payment')

            messages.warning(self.request, 'Failed To CheckOut')
            return redirect('cart:checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("cart:checkout")



def payment(request):
    try:
        order = get_object_or_404(Order, user=request.user, ordered=False)

        context = {
            'order':order,
        }

        return render(request, 'cart/payment.html', context)
    except:
        return redirect('cart:cart')



def payment_completed(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order.ordered = True
        order.save()

        for order_item in order.items.all():
            order_item.ordered = True
            order_item.save()

        messages.warning(request, 'Payment successfully done..')
        return render(request, 'cart/payment_done.html')

    except:
        messages.warning(request, 'Payment failed..')
        return redirect('cart:cart')


    messages.warning(request, 'Something went wrong..')
    return render(request, 'cart/payment_done.html')
