from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .models import OrderItem, Product, Seller, SellerUser, InventoryItem
from .forms import RegistrationForm, LoginForm, InventoryItemForm

def index(request):
    return HttpResponse("Hello, world. You're at the mercado-brasileiro app.")

def products_index(request):
    products_list = Product.objects.order_by("id")[:10]
    template = loader.get_template('products/index.html')
    context = { 'products_list': products_list }
    if request.user.is_authenticated:
        context['current_user'] = request.user
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
    print("logging in with: ", username, password)
    user = authenticate(username=username, password=password)
    if user is None:
        return render_login_form(request, form, error="Authentication Failed")
    else:
        login(request, user)
        return redirect("sellers_profile")

def sellers_logout(request):
    logout(request)
    return redirect("sellers_login")

def sellers_profile(request):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    page_size = 10
    page = int(request.GET.get('page') or 1)
    order_offset_low = page_size * (page - 1)
    order_offset_high = order_offset_low + page_size
    order_items = OrderItem.objects.filter(seller_uuid=seller.seller_uuid)[order_offset_low:order_offset_high]
    template = loader.get_template('sellers/profile.html')
    context = {'seller': seller, 'user': request.user, 'order_items': order_items}
    return HttpResponse(template.render(context, request))

def sellers_inventory(request):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    inventory_items = InventoryItem.objects.filter(seller_uuid=seller.seller_uuid).all()
    template = loader.get_template('sellers/inventory.html')
    context = {'seller': seller, 'user': request.user, 'inventory_items': inventory_items}
    return HttpResponse(template.render(context, request))

def inventory_new(request):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    template = loader.get_template('inventory/new.html')
    form = InventoryItemForm()
    context = { 'form': form }
    return HttpResponse(template.render(context, request))

def inventory_add(request):
    if request.method != 'POST':
        raise RuntimeError("Invalid Http Method")
    elif not request.user.is_authenticated:
        return redirect("sellers_login")
    # todo: write inventory item to DB
    return redirect("sellers_inventory")

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
                user = User.objects.create_user(uname, email, pw)
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

def render_login_form(request, form, error=None):
    template = loader.get_template('sellers/login.html')
    context = {'form': form, 'auth_err': error}
    return HttpResponse(template.render(context, request))