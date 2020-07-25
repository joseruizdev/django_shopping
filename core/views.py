from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Product

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