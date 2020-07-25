from django.contrib import admin
from core.models import Product, OrderProduct, Order

admin.site.site_header = 'Django Shopping'

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
