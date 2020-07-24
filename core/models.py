from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Product: {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(OrderProduct)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return f"Ordered by {self.user.username}"
