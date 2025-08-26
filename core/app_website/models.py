from django.db import models
from app_account.validators import CustomValidations


class ContactStatusType(models.IntegerChoices):
    not_read = 1, ('جدید')
    read = 2, ('خوانده شده')
    responded = 3, ('پاسخ داده شده')


class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    phone = models.CharField(max_length=11, validators=[CustomValidations.validate_phone_number])
    status = models.IntegerField(choices=ContactStatusType.choices, default=ContactStatusType.not_read.value)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_website_contact'
        ordering = ['-created_date']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} - ({self.email})"

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_website_newsletter'
        ordering = ['-created_date']

    def __str__(self):
        return self.email
