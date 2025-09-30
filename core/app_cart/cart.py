from app_shop.models import Product, ProductStatusType
from django.core.exceptions import ObjectDoesNotExist


class CartSession:

    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault('cart', self.get_empty_cart())

    @staticmethod
    def get_empty_cart():
        return {
            'items': [],          # [{'product_id': int, 'quantity': int}]
            'total_quantity': 0,
        }

    def save(self):
        self.session['cart'] = self._cart
        self.session.modified = True

    def clear(self):
        self._cart = self.get_empty_cart()
        self.save()

    def add_product(self, product_id):
        try:
            product = Product.objects.only('stock').get(pk=product_id)
        except ObjectDoesNotExist:
            # product doesn't exist — keep behavior similar to original (silent return)
            return

        stock = int(getattr(product, 'stock', 0)) or 0
        if stock <= 0:
            return

        # try to find existing item and update in-place
        for idx, item in enumerate(self._cart.get('items', [])):
            if item.get('product_id') == product_id:
                current_qty = int(item.get('quantity', 0))
                if current_qty < stock:
                    self._cart['items'][idx]['quantity'] = current_qty + 1
                    self._recalculate()
                # either incremented or already at stock limit — done
                return

        # product not in cart — add it
        self._cart.setdefault('items', []).append({
            'product_id': product_id,
            'quantity': 1
        })
        self._recalculate()

    def remove_product(self, product_id):
        for item in self._cart['items']:
            if item['product_id'] == product_id:
                print(item)
                self._cart['items'].remove(item)
                print(self._cart['items'])
                self._recalculate()
                return

    def change_product_quantity(self, product_id, quantity):
        for item in self._cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] = int(quantity)
                print(quantity)
                print(item)
                self._recalculate()
                return

    def _recalculate(self):
        self._cart['total_quantity'] = sum(item['quantity'] for item in self._cart['items'])
        self.save()

    def get_cart_items(self):
        """Return raw cart items (ids & quantities)."""
        return self._cart['items']

    def get_cart_item_quantity(self, product_id):
        for item in self._cart['items']:
            if item['product_id'] == str(product_id):
                return item['quantity']
        return False

    def get_cart_total_quantity(self):
        return self._cart['total_quantity']

    def get_cart_details(self, with_products=False):
        """
        Return cart details.
        - If with_products=True → includes actual Product objects (for templates).
        - Else → returns JSON-safe dict (for AJAX).
        """
        cart_total_price = 0
        cart_items = []

        for item in self._cart['items']:
            try:
                product = Product.objects.get(
                    id=item['product_id'],
                    status=ProductStatusType.publish.value
                )
                total_price = int(product.get_price) * item['quantity']

                if with_products:
                    # For templates → include real Product object
                    item_data = {
                        "product": product,
                        "quantity": item['quantity'],
                        "total_price": total_price,
                    }
                else:
                    # For JSON → product.id, name, etc. (serializable only)
                    item_data = {
                        "product_id": product.id,
                        "name": product.name,
                        "quantity": item['quantity'],
                        "total_price": total_price,
                    }

                cart_total_price += total_price
                cart_items.append(item_data)

            except Product.DoesNotExist:
                continue

        return {
            "cart_items": cart_items,
            "cart_total_price": cart_total_price,
            "cart_total_quantity": self._cart['total_quantity'],
        }

    def check_product_in_cart(self, product_id):
        for item in self._cart['items']:
            if item['product_id'] == str(product_id):
                return True
        return False

