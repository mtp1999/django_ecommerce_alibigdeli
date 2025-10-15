from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('app_account.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_cart_cart'
        ordering = ('-created_date',)

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('app_shop.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_cart_item'
        ordering = ('-created_date',)

    def __str__(self):
        return str(self.cart) + ':' + str(self.product) + ':' + str(self.quantity)
