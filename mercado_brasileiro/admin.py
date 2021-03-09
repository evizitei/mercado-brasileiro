from django.contrib import admin

from .models import Customer
from .models import GeoLocation
from .models import OrderItem
from .models import OrderPayment
from .models import OrderReview
from .models import Order
from .models import Product
from .models import Seller
from .models import CategoryNameTranslation

admin.site.register(Customer)
admin.site.register(GeoLocation)
admin.site.register(OrderItem)
admin.site.register(OrderPayment)
admin.site.register(OrderReview)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(CategoryNameTranslation)