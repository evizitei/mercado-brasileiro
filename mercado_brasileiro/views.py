from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .models import Product, Seller, SellerUser
from .forms import RegistrationForm, LoginForm

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


def sellers_register(request):
    return render_registration_form(request, RegistrationForm())

def sellers_login(request):
    form = LoginForm()
    return render_login_form(request, form)

def sellers_authenticate(request):
    if request.method != 'POST':
        return redirect("sellers_login")
    form = LoginForm(request.POST)
    print("FORM DATA: ", form.data)
    if not form.is_valid():
        return render_login_form(request, form)
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        return render_login_form(request, form)
    else:
        return redirect("sellers_profile")

def sellers_logout(request):
    logout(request)
    redirect("sellers_login")

def sellers_profile(request):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    template = loader.get_template('sellers/profile.html')
    context = {'seller': form, 'user': request.user}
    return HttpResponse(template.render(context, request))


def sellers_attach_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            seller_uuid = form.cleaned_data["seller_uuid"]
            seller = Seller.objects.get(seller_uuid=seller_uuid)
            uname = form.cleaned_data['name']
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            with transaction.atomic():
                user = User.objects.create_user(form.cleaned_data, email, pw)
                user.save()
                seller_user = SellerUser(
                    seller_uuid=seller.seller_uuid,
                    user_id=user.id
                )
                seller_user.save(force_insert=True)
            return redirect("sellers_login")
        else:
            return render_registration_form(request, form)

def render_registration_form(request, form):
    template = loader.get_template('sellers/register.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def render_login_form(request, form):
    template = loader.get_template('sellers/login.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))