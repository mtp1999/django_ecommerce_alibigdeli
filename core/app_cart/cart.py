from app_shop.models import Product, ProductStatusType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from app_cart.models import Cart, CartItem


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
        self._recalculate()
        for item in self._cart['items']:
            if item['product_id'] == str(product_id):
                return item['quantity']
        return False

    def get_cart_total_quantity(self):
        self._recalculate()
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

    def sync_db_session_post_login(self, user):
        """
        Merge session cart (self._cart['items']) into user's DB cart.
        Behaviour preserved:
          - If session item product not in cart -> create CartItem with session quantity
          - If product exists in cart -> replace cart quantity with session quantity
          - After merging, any cart items that were not present in session are appended
            to self._cart['items'] (as strings for product_id) with their DB quantity.
        """

        try:
            cart, _created = Cart.objects.get_or_create(user=user)
        except Exception as exc:
            # logger.exception("Failed to get_or_create Cart for user %r: %s", getattr(user, "pk", user), exc)
            return

        try:
            # Load existing CartItems for this cart in one query (also eager-load product)
            cart_items_qs = CartItem.objects.filter(cart=cart).select_related('product')
            cart_items_list = list(cart_items_qs)  # evaluate once
            # map by product id for O(1) lookup
            cart_items_map = {ci.product.id: ci for ci in cart_items_list}
            # maintain the same list-of-ids behavior as original code (order preserved)
            cart_items_ids = [ci.product.id for ci in cart_items_list]

            # collect pids that need Product lookup (new products)
            new_pids = set()
            # prepare containers for DB writes
            to_create = []
            to_update = []

            # iterate session items and decide create/update
            for sess_item in self._cart['items']:
                pid = int(sess_item.get('product_id'))
                qty = int(sess_item.get('quantity', 0))

                if pid not in cart_items_ids:
                    # new CartItem needed
                    new_pids.add(pid)
                else:
                    # existing: remove id from remaining list and prepare update
                    # keep behavior same as original: remove first occurrence
                    try:
                        cart_items_ids.remove(pid)
                    except ValueError:
                        # shouldn't happen, but be defensive
                        pass
                    existing_ci = cart_items_map.get(pid)
                    if existing_ci:
                        existing_ci.quantity = qty
                        to_update.append(existing_ci)

            # Fetch required Product objects in one query
            products_map = {}
            if new_pids:
                products_map = Product.objects.filter(id__in=new_pids).in_bulk()

            # Build CartItem instances to create (using already fetched Product objects)
            for sess_item in self._cart['items']:
                try:
                    pid = int(sess_item.get('product_id'))
                    qty = int(sess_item.get('quantity', 0))
                except Exception:
                    continue

                if pid in new_pids:
                    product = products_map.get(pid)
                    if not product:
                        # product doesn't exist in DB — skip (original code would raise and be swallowed)
                        # logger.debug("Product id %s not found in DB; skipping create.", pid)
                        continue
                    to_create.append(CartItem(cart=cart, product=product, quantity=qty))

            # Apply DB changes in a single transaction
            with transaction.atomic():
                if to_create:
                    CartItem.objects.bulk_create(to_create)
                if to_update:
                    # bulk_update needs the list of fields to update
                    CartItem.objects.bulk_update(to_update, ['quantity'])

            # Finally, append remaining cart items (those present in DB but not in session)
            for pid in cart_items_ids:
                ci = cart_items_map.get(pid)
                if not ci:
                    continue
                self._cart['items'].append({
                    'product_id': str(pid),
                    'quantity': ci.quantity
                })

            # persist session/cart as before
            self.save()

        except Exception as exc:
            # logger.exception("Failed to sync session cart to DB for user %r: %s", getattr(user, "pk", user), exc)
            return

    def sync_db_session_pre_logout(self, user):
        """
        Persist session cart to DB for `user`.
        Optimized: single query to load products, single bulk_create for items.
        """

        if not self._cart['items']:
            return

        try:
            cart, _created = Cart.objects.get_or_create(user=user)
        except Exception as exc:
            # logger.exception("Failed to get_or_create Cart for user %r: %s", getattr(user, "pk", user), exc)
            return

        # Remove existing items for this cart
        CartItem.objects.filter(cart=cart).delete()

        # Collect unique product ids from session cart (as ints)
        product_ids = [int(it['product_id']) for it in self._cart['items']]

        if not product_ids:
            return

        # Fetch all products in one query and map by id
        products_map = Product.objects.filter(id__in=product_ids).in_bulk()

        cart_items_to_create = []
        for it in self._cart['items']:
            pid = int(it.get('product_id'))
            qty = int(it.get('quantity', 0))

            product = products_map.get(pid)
            if product is None:
                # product not found in DB: skip (original code would error here)
                # logger.debug("Product id %s not found; skipping", pid)
                continue

            cart_items_to_create.append(
                CartItem(cart=cart, product=product, quantity=qty)
            )

        if not cart_items_to_create:
            return

        # Bulk create inside a transaction
        try:
            with transaction.atomic():
                CartItem.objects.bulk_create(cart_items_to_create)
        except Exception as exc:
            # logger.exception("Failed to bulk_create CartItems for cart %s: %s", getattr(cart, "pk", cart), exc)
            # depending on your needs, you may want to re-raise
            return
