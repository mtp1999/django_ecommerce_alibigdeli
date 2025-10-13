from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductStatusType(models.IntegerChoices):
    publish = 1, ('نمایش')
    draft = 2, ('عدم نمایش')


class ProductCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_shop_category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey('app_account.User', on_delete=models.PROTECT)
    category = models.ManyToManyField(to=ProductCategory, db_table='app_shop_product_category')
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(default='defaults/product.png', upload_to='products/main_image/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    description = models.TextField(null=True, blank=True)
    brief_description = models.TextField(null=True, blank=True, max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_shop_product'

    def __str__(self):
        return str(self.id) + '[' + str(self.title) + ']'

    @property
    def get_price(self):
        if not self.discount_percent:
            return self.price
        discount_amount = (self.price * self.discount_percent)/100
        price = self.price - discount_amount
        return int(price)

    def is_discounted(self):
        return False if self.discount_percent == 0 else True

    def is_published(self):
        if self.status == ProductStatusType.publish.value:
            return True
        return False


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

    class Meta:
        db_table = 'app_shop_product_image'

    def __str__(self):
        return str(self.id) + '-' + str(self.product.title)
