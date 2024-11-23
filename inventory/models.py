from django.db import models
from django.utils.timezone import now
from django.db.models import Sum
from django.apps import apps

# Category for organizing products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory1(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class SubCategory2(models.Model):
    sub_category1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Vendor(models.Model):
    name = models.CharField(max_length=200)

class SalesRep(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    vendor = models.ManyToManyField('Vendor', related_name="vendor", blank=True)

class Brand(models.Model):
    name = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rep = models.ManyToManyField('SalesRep', related_name="rep", blank=True)
    b2b = models.URLField(blank=True, null=True)
# Product with variants
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/product/', default='')
    # Reverse relationship (Optional) if not yet established
    items = models.ManyToManyField('Item', related_name="product_variants", blank=True)    
    
    def quantity_on_hand(self):
        return sum(variant.received_quantity() - variant.sold_quantity() for variant in self.variants.all())

    def quantity_on_order(self):
        return sum(variant.on_order_quantity() for variant in self.variants.all())

    def __str__(self):
        return self.name


# Product Variants for attributes like color, size, etc.
# Add a reverse relationship from ProductVariant to Item (if not already set up)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    attribute = models.CharField(max_length=100)  # e.g., "Color: Red, Size: M"
    details = models.CharField(max_length=100)  # e.g., "Color: Red, Size: M"
    sparrownumber = models.CharField(default=1)
    barcode = models.ImageField(upload_to='uploads/product/', default='')
    upc = models.IntegerField(default=1)
    lightspeedid = models.IntegerField(default=1)
    initial_quantity = models.PositiveIntegerField(default=0)    
# Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
# Add Purchase Stuff

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
    order_datercvd = models.DateTimeField(default=now)
    order_qty = models.PositiveIntegerField(default=0)
    rcvd_qty = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.product_variant.product.price



class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    on_hand = models.PositiveIntegerField(default=0)
    date_last_received = models.DateTimeField(default=now)

    @property
    def received_quantity(self):
        """
        Calculate the sum of received quantities from related OrderItems.
        """
        total_received = (
            OrderItem.objects.filter(product_variant=self.variant)
            .aggregate(Sum('rcvd_qty'))
            .get('rcvd_qty__sum', 0)
        )
        return total_received or 0

    @property
    def sold_quantity(self):
        """
        Calculate the sum of sold quantities from related SaleItems.
        """
        total_sold = (
            apps.get_model('sales', 'SaleItem')
            .objects.filter(item=self)
            .aggregate(Sum('quantity'))
            .get('quantity__sum', 0)
)


    def __str__(self):
        return f"{self.product.name} ({self.variant.attribute}) - Quantity: {self.on_hand}"

class Label(models.Model):
    item = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='labels')  # Refers to the Product model
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='labels')  # Refers to the Brand model
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Direct price field (not ForeignKey to Product)
    barcode = models.CharField(max_length=50)  # Direct barcode field (not ForeignKey to Product)

    def __str__(self):
        return f"{self.brand.name}: {self.item.name} - {self.price} - {self.barcode}"

