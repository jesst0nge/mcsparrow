from django.shortcuts import render, redirect
from .models import Sale, SaleItem
from inventory.models import Product
from django.db import transaction
from django.contrib import messages

def new_sale(request):
    products = Product.objects.all()

    if request.method == "POST":
        try:
            with transaction.atomic():
                # Create a new Sale instance
                sale = Sale.objects.create()

                for product in products:
                    quantity_str = request.POST.get(f'quantity_{product.id}', '0')
                    try:
                        quantity = int(quantity_str)
                    except ValueError:
                        quantity = 0

                    if quantity > 0:
                        if product.stock >= quantity:
                            SaleItem.objects.create(sale=sale, product=product, quantity=quantity)
                            product.stock -= quantity
                            product.save()
                        else:
                            messages.error(request, f"Not enough stock for {product.name}.")
                            return redirect('sales:new_sale')

                messages.success(request, "Sale completed successfully!")
                return render(request, 'sales/sale.html', {'sale': sale})
        except Exception as e:
            messages
            
def search_view(request):
    return render(request, 'sales/search.html')  # Adjust to your template
