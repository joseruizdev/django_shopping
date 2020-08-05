from django.urls import path
from core.views import HomeView, CartView, ShopView, ProductView, add_to_cart, remove_from_cart, remove_one_product_from_cart

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('products/<slug>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-one-product-from-cart/<slug>/', remove_one_product_from_cart, name='remove-one-product-from-cart'),
]