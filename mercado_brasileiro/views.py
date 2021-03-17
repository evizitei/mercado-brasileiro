from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader

from .models import Product, GeoLocation
from .forms import RegistrationForm

def index(request):
    return HttpResponse("Hello, world. You're at the mercado-brasileiro app.")

def products_index(request):
    products_list = Product.objects.order_by("id")[:10]
    template = loader.get_template('products/index.html')
    context = { 'products_list': products_list }
    return HttpResponse(template.render(context, request))

def products_show(request, product_id):
    product = Product.objects.get(pk=product_id)
    template = loader.get_template('products/show.html')
    context = { 'product': product }
    return HttpResponse(template.render(context, request))

def visualization(request):
    location = GeoLocation.objects.order_by("zip_code_prefix")[:10]
    template = loader.get_template('visualizations/index.html')
    context = { 'location': location }
    return HttpResponse(template.render(context, request))


def sellers_register(request):
    template = loader.get_template('sellers/register.html')
    form = RegistrationForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def sellers_attach_user(request):
    # Create user and save to the database
    user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

    # Update fields and then save again
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
