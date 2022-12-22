from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from cart.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import ProductFilter


# Create your views here.
@login_required(login_url = 'account:login')
def new_arrival(request):
    return render(request, 'products/new_arrival_products.html')






@login_required(login_url = 'account:login')
def products_home(request):

    all_category = Category.objects.all()


    if request.method == 'POST':
        if 'search_product' in request.POST:
            search = request.POST['search_product']
            if search != '':
                all_products_fashion = Product.objects.filter(product_name__icontains=search)
            else:
                all_products_fashion = Product.objects.all()
    else:
        all_products_fashion = Product.objects.all()
        all_products_filter = ProductFilter(request.GET, queryset=all_products_fashion)
        all_products_fashion = all_products_filter.qs
        print(all_products_fashion)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(all_products_fashion, 12)

    try:
        all_products_fashion = paginator.page(page_num)
    except PageNotAnInteger:
        all_products_fashion = paginator.page(1)
    except EmptyPage:
        all_products_fashion = paginator.page(paginator.num_pages)


    context = {
        'all_products_fashion':all_products_fashion,
        'all_category':all_category,
        'all_products_filter':all_products_filter,
    }
    return render(request, 'products/products_home.html', context)




@login_required(login_url = 'account:login')
def product_detail(request, id):
    single_product = get_object_or_404(Product, id=id)


    if request.method == 'POST':
        product_id = request.POST['product_id']
        product_quntity = request.POST['quantity']


        try:
            item = get_object_or_404(Product, id=product_id)
            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user = request.user,
                ordered = False

            )

            if created:
                order_item.quantity = int(product_quntity)
                order_item.save()


            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                #check if order item in the order
                if order.items.filter(item__id=item.id).exists():
                    order_item.quantity += int(product_quntity)
                    order_item.save()
                    messages.info(request, 'This item quantity was updated to your cart')
                else:
                    messages.info(request, 'This item was added to your cart')
                    order.items.add(order_item)
                    order_item.quantity = int(product_quntity)
                    order_item.save()
            else:
                order = Order.objects.create(user=request.user)
                order.items.add(order_item)
                messages.info(request, 'This item was added to your cart')
        except Exception as e:
            print(e)

    context = {
        'single_product':single_product,
    }

    return render(request, 'products/product_detail.html', context)






def add_to_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_item, _ = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False

    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect('products:products_page')








def remove_from_cart(request, id):
    item = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered = False

    )
    if order_qs.exists():
        order = order_qs[0]
        #check if order item in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'This item was removed from your cart')
            return redirect('cart:cart')
        else:
            messages.info(request, 'This item was not in  your cart')
            return redirect('cart:cart')
    else:
        messages.info(request, 'You do not have an activate order')
        return redirect('cart:cart')
