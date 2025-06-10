import re


class CustomValidations:

    @staticmethod
    def validate_phone_number(number):
        return bool(re.fullmatch("^\+989[0-9]{9}$", number))

    @staticmethod
    def validate_national_id(nid):
        """ National ID must contains 10 digits(in Iran) """
        return bool(re.fullmatch(r"^\d{10}$", nid))

    @staticmethod
    def validate_name_en(name):
        return bool(re.fullmatch(r"^[A-Za-z]+$", name))

    @staticmethod
    def validate_name_fa(name):
        return bool(re.fullmatch(r"^[آ-ی]+$", name))


if __name__ == '__main__':

    # validate phone number
    print(CustomValidations.validate_phone_number('+989102690080'))

    # validate national ID
    print(CustomValidations.validate_national_id('0022042019'))

    # validate name english
    print(CustomValidations.validate_name_en('Jackie'))

    # validate name farsi
    print(CustomValidations.validate_name_fa('سمیه'))
