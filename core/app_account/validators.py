import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomValidations:

    @staticmethod
    def validate_phone_number(number):
        if not re.fullmatch("^09[0-9]{9}$", number):
            raise ValidationError(
                _('phone number is wrong.'),
            )
