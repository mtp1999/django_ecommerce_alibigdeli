from django import forms
from app_account.models import Profile
from app_shop.models import Product


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'phone_number']


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # OR add a specific class to one field
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['brief_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['stock'].widget.attrs.update({'type': 'number', 'class': 'form-control'})
        self.fields['discount_percent'].widget.attrs.update({'type': 'number', 'class': 'form-control', 'min': 0, 'max': 100})
        self.fields['price'].widget.attrs.update({'type': 'number', 'class': 'form-control', 'min': 0})


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'title',
            'slug',
            'image',
            'stock',
            'price',
            'discount_percent',
            'status',
            'description',
            'brief_description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # OR add a specific class to one field
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['brief_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['stock'].widget.attrs.update({'type': 'number', 'class': 'form-control'})
        self.fields['discount_percent'].widget.attrs.update({'type': 'number', 'class': 'form-control', 'min': 0, 'max': 100})
        self.fields['price'].widget.attrs.update({'type': 'number', 'class': 'form-control', 'min': 0})
