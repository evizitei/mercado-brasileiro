"""mercado_brasileiro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_index, name='index'),
    path('admin/', admin.site.urls),
    path('products/', views.products_index, name="products_index"),
    path('products/<int:product_id>', views.products_show, name="product_show"),
    path('sellers/register', views.sellers_register, name="sellers_register"),
    path('sellers/attach', views.sellers_attach_user, name="sellers_attach_user"),
    path('sellers/login', views.sellers_login, name="sellers_login"),
    path('sellers/auth', views.sellers_authenticate, name="sellers_auth"),
    path('sellers/profile', views.sellers_profile, name="sellers_profile"),
    path('sellers/inventory', views.sellers_inventory, name="sellers_inventory"),
    path('inventory/new', views.inventory_new, name="inventory_new"),
    path('inventory/add', views.inventory_add, name="inventory_add"),
    path('logout', views.sellers_logout, name="seller_logout")
]
