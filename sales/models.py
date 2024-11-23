from django.db import models
from inventory.models import *
from django.contrib.auth.models import User


# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return sum(item.total_price() for item in self.saleitem_set.all())

    def gst(self):
        return self.subtotal() * 0.05  # 5% GST

    def pst(self):
        return self.subtotal() * 0.07  # 7% PST

    def total_price(self):
        return self.subtotal() + self.gst() + self.pst()

    def __str__(self):
        return f"Sale #{self.id} - {self.created_at}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.item.price * self.quantity

class Discount(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.item.price * self.quantity

