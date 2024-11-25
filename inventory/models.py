from django.db import models
from django.utils.timezone import now
from django.db.models import Sum
from django.apps import apps

# Category for organizing products
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class SubCategory1(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories1")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory2(models.Model):
    sub_category1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE, related_name="subcategories2")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SalesRep(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    vendor = models.ManyToManyField('Vendor', related_name="sales_reps", blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rep = models.ManyToManyField(SalesRep, related_name="brands", blank=True)
    b2b = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# Product with variants
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, related_name="products", blank=True)
    subcat1 = models.ManyToManyField(SubCategory1, related_name="products", blank=True)
    subcat2 = models.ManyToManyField(SubCategory2, related_name="products", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True)

    def quantity_on_hand(self):
        return sum(variant.received_quantity - variant.sold_quantity for variant in self.variants.all())

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    attribute = models.CharField(max_length=100)  # e.g., "Color: Red, Size: M"
    details = models.CharField(max_length=100, blank=True)  # e.g., "Size: M"
    sparrownumber = models.CharField(max_length=100, default="N/A")
    barcode = models.CharField(max_length=50, default="N/A")
    upc = models.CharField(max_length=12, default="000000000000")
    lightspeedid = models.IntegerField(default=0)
    initial_quantity = models.PositiveIntegerField(default=0)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def on_order_quantity(self):
        return max(0, self.initial_quantity - self.received_quantity)

    def __str__(self):
        return f"{self.product.name} - {self.attribute}"

    class Meta:
        get_latest_by = "id"


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
    product_variant = models.ForeignKey(ProductVariant, null=True, on_delete=models.SET_NULL)
    order_datercvd = models.DateTimeField(default=now)
    order_qty = models.PositiveIntegerField(default=0)
    rcvd_qty = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.order_qty * self.product_variant.product.price

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product_variant}"


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    on_hand = models.PositiveIntegerField(default=0)
    date_last_received = models.DateTimeField(default=now)

    @property
    def received_quantity(self):
        total_received = OrderItem.objects.filter(product_variant=self.variant).aggregate(Sum('rcvd_qty')).get('rcvd_qty__sum', 0)
        return total_received or 0

    @property
    def sold_quantity(self):
        total_sold = apps.get_model('sales', 'SaleItem').objects.filter(item=self).aggregate(Sum('quantity')).get('quantity__sum', 0)
        return total_sold or 0

    def __str__(self):
        return f"{self.product.name} ({self.variant.attribute}) - Quantity: {self.on_hand}"


class Label(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='labels')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='labels')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand.name}: {self.item.product.name} - {self.price} - {self.barcode}"
