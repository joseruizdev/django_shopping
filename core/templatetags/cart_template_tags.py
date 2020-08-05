from django import template
from core.models import Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        queryset = Order.objects.filter(user=user, ordered=False)
        if queryset.exists():
            return queryset[0].products.count()
    else:
        return 0

@register.filter
def get_count_of_products(user):
    if user.is_authenticated:
        if Order.objects.filter(user=user, ordered=False).exists():
            order = Order.objects.get(user=user, ordered=False)
            if order:
                quantitites = order.products.all().values('quantity')
                products_count = 0
                for quantity in quantitites:
                    products_count += quantity.get('quantity')
                return products_count
            else:
                return 0
        else:
            return 0
    else:
        return 0