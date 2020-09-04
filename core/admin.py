from django.contrib import admin
from core.models import Product, OrderProduct, Order, Category

admin.site.site_header = 'Django Shopping'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'label')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Order)
