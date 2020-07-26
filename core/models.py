from django.db import models
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sports Wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('new', 'New'),
    ('sold-out', 'Sold Out')
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # TODO: Category Model and foreign key
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, blank=True, null=True)
    slug = models.SlugField(default='product-slug')

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

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return f"Ordered by {self.user.username}"
