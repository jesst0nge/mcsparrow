from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from .models import ProductVariant, Order
from django.db import transaction
from .forms import ItemForm
from django.http import JsonResponse
from django.contrib import messages

def category_summary(request):
	categories = Category.objects.all()
 
	return render(request, 'category_summary.html', {"categories":categories})

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Item.objects.filter(category=category)
		return render(request, 'category.html', {'item':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')

def product_search(request):
    query = request.GET.get('q', '')
    products = Item.objects.filter(name__icontains=query) if query else Item.objects.all()
    return render(request, 'inventory/product_search.html', {'item': products, 'query': query})


def product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'inventory/product_page.html', {'product': product})

def order_page(request):
    if request.method == "POST":
        # Handle new order creation (skipping for brevity here)
        pass

    return render(request, 'inventory/order_page.html', {'vendors': ["Vendor A", "Vendor B", "Vendor C"]})



def inventory_home(request):
    return render(request, 'inventory/inventory_home.html')


def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_home')  # Replace with your desired redirect URL
    else:
        form = ItemForm()
    return render(request, 'inventory/add_item.html', {'form': form})

def api_get_variants(request, product_id):
    variants = ProductVariant.objects.filter(product_id=product_id)
    data = {'variants': [{'id': v.id, 'attribute': v.attribute} for v in variants]}
    return JsonResponse(data)
