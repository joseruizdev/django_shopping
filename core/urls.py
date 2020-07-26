from django.urls import path
from core.views import ShopView, ProductView, add_to_cart, remove_from_cart

app_name = 'core'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('products/<slug>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
]