from django.urls import path
from core.views import home_view, ProductsByCategoryListView, CartView, CheckoutView, ShopView, ProductView, add_to_cart, remove_from_cart, remove_one_product_from_cart

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('category/<slug>/', ProductsByCategoryListView.as_view(), name='products-by-category'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('products/<slug>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-one-product-from-cart/<slug>/', remove_one_product_from_cart, name='remove-one-product-from-cart'),
]