from django.shortcuts import render, get_object_or_404
from .cart import Cart
from sales.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response

def cart_update(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        discount_code = request.POST.get('discount_code', '')

        # Update the cart with the new quantity
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.update(product, product_qty)

        # Calculate the new total with the discount code if provided
        total = cart.cart_total(discount_code)

        # Respond with the updated cart total
        return JsonResponse({'status': 'success', 'new_total': total})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})