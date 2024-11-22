from django.db import models
from django.utils.timezone import now

# Category for organizing products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Product with variants
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/product/', default='')

    def quantity_on_hand(self):
        return sum(variant.received_quantity() - variant.sold_quantity() for variant in self.variants.all())

    def quantity_on_order(self):
        return sum(variant.on_order_quantity() for variant in self.variants.all())

    def __str__(self):
        return self.name


# Product Variants for attributes like color, size, etc.
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    attribute = models.CharField(max_length=100)  # e.g., "Color: Red, Size: M"
    initial_quantity = models.PositiveIntegerField(default=0)
    received_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    date_last_received = models.DateTimeField(default=now)
    # Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def on_order_quantity(self):
        return max(0, self.initial_quantity - self.received_quantity)

    def __str__(self):
        return f"{self.product.name} - {self.attribute}"
    
    class Meta:
        get_latest_by = "date_last_received"


# Orders for purchasing products
class Order(models.Model):
    vendor = models.CharField(max_length=200)
    sales_rep = models.CharField(max_length=200, blank=True)
    order_date = models.DateTimeField(default=now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    discount_percent = models.FloatField(default=0.0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def total_order_value(self):
        total = sum(item.total_price() for item in self.orderitem_set.all())
        discount = total * (self.discount_percent / 100)
        return total - discount + self.shipping_cost

    def __str__(self):
        return f"Order #{self.id} - {self.vendor} ({self.order_date.date()})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.product_variant.product.price

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} ({self.variant.attribute}) - Quantity: {self.quantity}"
