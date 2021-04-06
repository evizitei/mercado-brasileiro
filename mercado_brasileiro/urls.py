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
    path('products/search', views.products_search, name="products_search"),
    path('products/<int:product_id>', views.products_show, name="product_show"),
    path('customers/register', views.customers_register, name="customers_register"),
    path('customers/attach', views.customers_attach_user, name="customer_attach_user"),
    path('customers/login', views.customers_login, name="customers_login"),
    path('customers/auth', views.customers_authenticate, name="customers_auth"),
    path('customers/profile', views.customers_profile, name="customers_profile"),
    path('sellers/register', views.sellers_register, name="sellers_register"),
    path('sellers/attach', views.sellers_attach_user, name="sellers_attach_user"),
    path('sellers/login', views.sellers_login, name="sellers_login"),
    path('sellers/auth', views.sellers_authenticate, name="sellers_auth"),
    path('sellers/profile', views.sellers_profile, name="sellers_profile"),
    path('sellers/inventory', views.sellers_inventory, name="sellers_inventory"),
    path('inventory/new', views.inventory_new, name="inventory_new"),
    path('inventory/add', views.inventory_add, name="inventory_add"),
    path('inventory/<int:inventory_item_id>/destroy', views.inventory_destroy, name="inventory_destroy"),
    path('inventory/<int:inventory_item_id>/edit', views.inventory_edit, name="inventory_edit"),
    path('inventory/<int:inventory_item_id>/update', views.inventory_update, name="inventory_update"),
    path('orders/<int:order_id>/detail', views.order_details, name="order_details"),
    path('orders/<int:order_id>/reviews/write', views.write_review, name="write_review"),
    path('orders/<int:order_id>/reviews/post', views.post_review, name="post_review"),
    path('logout', views.logout_action, name="logout").
    path('visualizations/', views.visualization, name="visualization"),
    path('visualizations/<str:product_type>/<int:price_min>/<int:price_max>/', views.visualization_update, name="visualization_update")
]
