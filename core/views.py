from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from core.models import Product, OrderProduct, Order
from django.utils import timezone
from django.contrib import messages

class HomeView(ListView):
    model = Product
    template_name = 'home.html'

def product_list(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "shop.html", context)

class ShopView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'shop.html'

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect("/")

class ProductView(DetailView):
    model = Product
    template_name = 'product-detail.html'

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # order_product = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        # Get the first element in the queryset.
        order = order_queryset[0]
        # Check if the OrderProduct is in the order.
        if order.products.filter(product__pk=product.pk).exists():
            # If exists, get the OrderProduct.
            order_product = order.products.filter(product__pk=product.pk).get()
            # Add 1 to OrderProduct.quantity.
            order_product.quantity += 1
            # Save the OrderProduct.
            order_product.save()
            messages.info(request, "The product quantity was updated!")
        else:
            # If the OrderProduct doesn't exist, then create one.
            order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False)
            # Add the OrderProduct to the Order.
            order.products.add(order_product)
            messages.success(request, "The product was added to your cart!")
    else:
        # If the OrderProduct doesn't exist, then create one.
        order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False)
        # Set the ordered_date of the order to current time.
        ordered_date = timezone.now()
        # If the Order doesn't exist, then create one.
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        # Add the OrderProduct to the Order.
        order.products.add(order_product)
        messages.success(request, "The product was added to your cart!")
    return redirect("core:cart")

# This function removes the OrderProduct from Order, but the OrderProduct still exists.
@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        # Check if the OrderProduct is in the order
        if order.products.filter(product__pk=product.pk).exists():
            # If exists, get the OrderProduct.
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            # Remove OrderProduct from Order
            # order.products.remove(order_product)
            order_product.delete()
            messages.warning(request, "This item was removed from your cart!")
        else:
            messages.error(request, "This item wasn't in your cart!")
            return redirect("core:product", slug=slug)
    else:
        messages.error(request, "You don't have an active order!")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)

@login_required
def remove_one_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # order_product = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        # Get the first element in the queryset.
        order = order_queryset[0]
        # Check if the OrderProduct is in the order.
        if order.products.filter(product__pk=product.pk).exists():
            order_product = order.products.filter(product__pk=product.pk).get()
            if order_product.quantity <= 1:
                order_product.delete()
            else:
                order_product.quantity -= 1
                # Save the OrderProduct.
                order_product.save()
            messages.info(request, "The product quantity was updated!")
            return redirect("core:cart")
        else:
            messages.info(request, "This product wasn't in your cart!")
            return redirect("core:cart")
    else:
        messages.success(request, "This product was added to yor cart!")
        return redirect("core:cart")