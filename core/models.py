from django.db import models
from django.conf import settings
from django.shortcuts import reverse

LABEL_CHOICES = (
    ('new', 'New'),
    ('sold-out', 'Sold Out')
)

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', null=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'core:products-by-category',
            kwargs={
                'slug': self.slug
            }
        )

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, blank=True, null=True)
    slug = models.SlugField(default='product-slug')
    image_1 = models.ImageField(null=True, upload_to='products')
    image_2 = models.ImageField(null=True, blank=True, upload_to='products')
    image_3 = models.ImageField(null=True, blank=True, upload_to='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'core:product',
            kwargs={
                'slug': self.slug
            }
        )
    
    def get_add_to_cart_url(self):
        return reverse(
            "core:add-to-cart",
            kwargs={
                'slug': self.slug
            }
        )
    
    def get_remove_from_cart_url(self):
        return reverse(
            "core:remove-from-cart",
            kwargs={
                'slug': self.slug
            }
        )

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_product_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        if self.product.discount_price:
            return self.get_total_product_price() - self.get_total_product_discount_price()
        else:
            return 0
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_product_discount_price()
        else:
            return self.get_total_product_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,  blank=True, null=True)

    def __str__(self):
        return f"Ordered by {self.user.username}"

    def get_amount_to_pay(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total
    
    def get_total_saved(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_amount_saved()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    street = models.CharField(max_length=100)
    internal_number = models.CharField(max_length=5, blank=True, null=True)
    external_number = models.CharField(max_length=5)
    suburb = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username