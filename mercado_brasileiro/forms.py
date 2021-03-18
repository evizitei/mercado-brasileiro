from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Product, Seller

class RegistrationForm(forms.Form):
  name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }), label='username')
  email = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }),label='email')
  pw = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control" }), label='password')
  pwc = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control" }), label='password confirmation')
  seller_uuid = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }),label='seller_uuid')

  def clean(self):
    cleaned_data = super().clean()
    if cleaned_data.get("pw") != cleaned_data.get("pwc"):
      raise ValidationError("password and confirmation must match")
    uuid = cleaned_data.get("seller_uuid")
    try:
      seller = Seller.objects.get(seller_uuid=uuid)
    except ObjectDoesNotExist:
      raise ValidationError("must provide a valid seller ID")


class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }), label='username')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control" }), label='password')
