from django.shortcuts import render
from .models import Sale, SaleItem
from inventory.models import Product
from django.db import transaction

def new_sale(request):
    products = Product.objects.all()
    sale = None

    if request.method == "POST":
        with transaction.atomic():
            # Create a new Sale instance
            sale = Sale.objects.create()
            for product in products:
                quantity = int(request.POST.get(f'quantity_{product.id}', 0))
                if quantity > 0:
                    SaleItem.objects.create(sale=sale, product=product, quantity=quantity)
                    product.stock -= quantity
                    product.save()

        # Pass the sale to the template for confirmation
        return render(request, 'sales/sale.html', {'sale': sale})

    return render(request, 'sales/new_sale.html', {'products': products})

# sales/views.py
def search_view(request):
    # Your search logic here
    return render(request, 'search.html')  # Adjust to your template
