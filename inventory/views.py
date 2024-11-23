from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import ProductVariant, Order
from django.db import transaction
from .forms import ItemForm
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from weasyprint import HTML

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

from django.http import JsonResponse

def subcategories(request, category_id):
    subcategories = SubCategory1.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def subcategories_level2(request, subcategory1_id):
    subcategories = SubCategory2.objects.filter(sub_category1_id=subcategory1_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def product_search(request):
    query = request.GET.get('q', '')
    products = Item.objects.filter(name__icontains=query) if query else Item.objects.all()
    return render(request, 'product_search.html', {'item': products, 'query': query})


def product_page(request, product_id):
    # Fetch the product based on its ID
    product = get_object_or_404(Product, id=product_id)
    
    # Fetch the selected variant from the GET parameters
    selected_variant = None
    if 'variant' in request.GET:
        variant_id = request.GET['variant']
        selected_variant = get_object_or_404(ProductVariant, id=variant_id)
    
    # Pass the product and selected_variant to the template
    return render(
        request,
        'inventory/product_page.html',
        {'product': product, 'selected_variant': selected_variant}
    )


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


def add_label(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_view')  # Redirect to ticket page
    else:
        form = LabelForm()
    return render(request, 'label_form.html', {'form': form})

def print_ticket(request):
    template = get_template('ticket.html')
    html = template.render({'data': 'Example Data'})
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
    return response

def done_button(request):
    return redirect('invenntory_home')
