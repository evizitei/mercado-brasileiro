from django.http import HttpResponse
from django.template import loader

from .models import Product, GeoLocation

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