from django.shortcuts import render
from core.models import Product

def product_list(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "product_list.html", context)
