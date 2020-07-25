from django.urls import path
from core.views import ShopView, ProductView

app_name = 'core'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('products/<slug>/', ProductView.as_view(), name='product')
]