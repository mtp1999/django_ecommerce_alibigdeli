from django import forms
from app_account.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'phone_number']
