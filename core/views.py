from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from core.models import Product, OrderProduct, Order
from django.utils import timezone
from django.contrib import messages

def product_list(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "shop.html", context)

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'

class ProductView(DetailView):
    model = Product
    template_name = 'product-detail.html'

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        # check if the OrderProduct is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = order.products.filter(product__pk=product.pk).get()
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "The product quantity was updated!")
        else:
            order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False)
            order.products.add(order_product)
            messages.success(request, "The product was added to your cart!")
    else:
        order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False)
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.success(request, "The product was added to your cart!")
    return redirect("core:product", slug=slug)