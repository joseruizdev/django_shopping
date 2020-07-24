from django.urls import path
from core.views import product_list

app_name = 'core'

urlpatterns = [
    path('', product_list, name='product-list'),
]