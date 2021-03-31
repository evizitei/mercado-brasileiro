from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

<<<<<<< HEAD
from .models import OrderItem, Product, Seller, SellerUser GeoLocation, InventoryItem
from .forms import RegistrationForm, LoginForm, InventoryItemForm
||||||| merged common ancestors
from .models import OrderItem, Product, Seller, SellerUser, InventoryItem
from .forms import RegistrationForm, LoginForm, InventoryItemForm
=======
from .models import OrderItem, Product, Seller, SellerUser, InventoryItem
from .forms import RegistrationForm, LoginForm, InventoryItemForm, ProductSearchForm
>>>>>>> 30f7752566fad7320075dd5f63fa4c2976ce8ff4

def index(request):
    return HttpResponse("Hello, world. You're at the mercado-brasileiro app.")

def products_index(request):
    products_list = Product.objects.order_by("id")[:10]
    template = loader.get_template('products/index.html')
    form = ProductSearchForm()
    context = { 'products_list': products_list, 'search_form': form }
    if request.user.is_authenticated:
        context['current_user'] = request.user
    return HttpResponse(template.render(context, request))

def products_search(request):
    if request.method != 'POST':
        return redirect("products_index")
    form = ProductSearchForm(request.POST)
    template = loader.get_template('products/index.html')
    context = { 'products_list': [], 'search_form': form }
    if request.user.is_authenticated:
        context['current_user'] = request.user
    if form.is_valid():
        term = form.cleaned_data['search_term']
        products_list = Product.objects.filter(category_name__icontains=term)
        context['products_list'] = products_list[:10]
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
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    form = InventoryItemForm(request.POST)
    if form.is_valid():
        status = form.cleaned_data['status']
        item = InventoryItem(
            seller_uuid=seller.seller_uuid,
            product_uuid=form.cleaned_data["product_uuid"],
            name=form.cleaned_data["name"],
            owned=(status=="1"),
            available=(status=="2"),
            wholesale_unit_price=form.cleaned_data['wholesale_unit_price'],
            count=form.cleaned_data['count']
        )
        item.save(force_insert=True)
        return redirect("sellers_inventory")
    else:
        template = loader.get_template('inventory/new.html')
        form = InventoryItemForm()
        context = { 'form': form }
        return HttpResponse(template.render(context, request))

def inventory_edit(request, inventory_item_id):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    item = InventoryItem.objects.get(pk=inventory_item_id)
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    if not item.seller_uuid == seller.seller_uuid:
        return HttpResponse('Unauthorized', status=401)
    status = '1'
    if item.available:
        status = '2'
    form = InventoryItemForm({
        'product_uuid': item.product_uuid,
        'name': item.name,
        'status': status,
        'wholesale_unit_price': item.wholesale_unit_price,
        'count': item.count
    })
    template = loader.get_template('inventory/edit.html')
    context = { 'form': form, 'inventory_item': item }
    return HttpResponse(template.render(context, request))

def inventory_update(request, inventory_item_id):
    if request.method != 'POST':
        raise RuntimeError("Invalid Http Method")
    elif not request.user.is_authenticated:
        return redirect("sellers_login")
    item = InventoryItem.objects.get(pk=inventory_item_id)
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    if not item.seller_uuid == seller.seller_uuid:
        return HttpResponse('Unauthorized', status=401)
    form = InventoryItemForm(request.POST)
    if form.is_valid():
        status = form.cleaned_data['status']
        item.product_uuid=form.cleaned_data["product_uuid"]
        item.name=form.cleaned_data["name"]
        item.owned=(status=="1")
        item.available=(status=="2")
        item.wholesale_unit_price=form.cleaned_data['wholesale_unit_price']
        item.count=form.cleaned_data['count']
        item.save()
        return redirect("sellers_inventory")
    else:
        template = loader.get_template('inventory/edit.html')
        form = InventoryItemForm()
        context = { 'form': form }
        return HttpResponse(template.render(context, request))

def inventory_destroy(request, inventory_item_id):
    if not request.user.is_authenticated:
        return redirect("sellers_login")
    item = InventoryItem.objects.get(pk=inventory_item_id)
    seller_user = SellerUser.objects.get(user_id=request.user.id)
    seller = Seller.objects.get(seller_uuid=seller_user.seller_uuid)
    if not item.seller_uuid == seller.seller_uuid:
        return HttpResponse('Unauthorized', status=401)
    item.delete()
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

    # Update fields and then save again
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()

def render_login_form(request, form, error=None):
    template = loader.get_template('sellers/login.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))
