from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Discount)