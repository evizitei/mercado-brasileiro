from django import forms

class RegistrationForm(forms.Form):
  name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }), label='username')
  email = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }),label='email')
  pw = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control" }), label='password')
  pwc = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control" }), label='password confirmation')
  seller_uuid = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control" }),label='seller_uuid')