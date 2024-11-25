from django.shortcuts import render, get_object_or_404
from .cart import Cart
from inventory.models import Item
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_item = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_item":cart_item, "quantities":quantities, "totals":totals})

def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		item_id = int(request.POST.get('item_id'))
		item_qty = int(request.POST.get('item_qty'))

		# lookup item in DB
		item = get_object_or_404(item, id=item_id)
		
		# Save to session
		cart.add(item=item, quantity=item_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("item Added To Cart..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		item_id = int(request.POST.get('item_id'))
		# Call delete Function in Cart
		cart.delete(item=item_id)

		response = JsonResponse({'item':item_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response

def cart_update(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_qty = int(request.POST.get('item_qty'))
        discount_code = request.POST.get('discount_code', '')

        # Update the cart with the new quantity
        cart = Cart(request)
        item = item.objects.get(id=item_id)
        cart.update(item, item_qty)

        # Calculate the new total with the discount code if provided
        total = cart.cart_total(discount_code)

        # Respond with the updated cart total
        return JsonResponse({'status': 'success', 'new_total': total})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})