from store.models import Profile, Discount  # Assuming you have a Discount model
from inventory.models import Item

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, item, quantity):
        item_id = str(item)
        item_qty = str(quantity)
        if item_id not in self.cart:
            self.cart[item_id] = int(item_qty)
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, item, quantity):
        item_id = str(item.id)
        item_qty = str(quantity)
        if item_id not in self.cart:
            self.cart[item_id] = int(item_qty)
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def cart_total(self, discount_code=None):
        item_ids = self.cart.keys()
        items = item.objects.filter(id__in=item_ids)
        quantities = self.cart
        total = 0
        
        for key, value in quantities.items():
            key = int(key)
            for item in items:
                if item.id == key:
                    if item.is_sale:
                        total += (item.sale_price * value)
                    else:
                        total += (item.price * value)
        
        # If a discount code is provided, apply it
        if discount_code:
            discount_amount = self.apply_discount(discount_code)
            total -= total * (discount_amount / 100)  # Apply discount percentage
        
        return total

    def apply_discount(self, discount_code):
        """Method to check discount code validity and return discount percentage."""
        try:
            discount = Discount.objects.get(code=discount_code, active=True)
            return discount.value  # Assuming discount.value stores the percentage value of the discount
        except Discount.DoesNotExist:
            return 0  # No discount applied if the code is invalid or expired

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        return items

    def get_quants(self):
        return self.cart

    def update(self, item, quantity):
        item_id = str(item)
        item_qty = int(quantity)
        self.cart[item_id] = item_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        return self.cart

    def delete(self, item):
        item_id = str(item)
        if item_id in self.cart:
            del self.cart[item_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("\'", "\"")
            current_user.update(old_cart=str(carty))
