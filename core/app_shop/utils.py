from django.db.models import ExpressionWrapper, fields
from django.db.models import F


# def calculate_final_price(price, discount_percent):
#     final_price =
#     return final_price


custom_calc = ExpressionWrapper(
    F('price') - ((F('price') * F('discount_percent')) / 100),
    output_field=fields.IntegerField()
)