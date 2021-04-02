from django.db import models

class Customer(models.Model):
  uuid = models.CharField(max_length=200)
  unique_id = models.CharField(max_length=200)
  zip_code_prefix = models.CharField(max_length=20)
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=30)

class GeoLocation(models.Model):
  zip_code_prefix = models.CharField(max_length=20)
  lat = models.FloatField()
  lng = models.FloatField()
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=30)

class OrderItem(models.Model):
  order_uuid = models.CharField(max_length=50)
  order_item_id = models.IntegerField()
  product_uuid = models.CharField(max_length=50)
  seller_uuid = models.CharField(max_length=50)
  shipping_limit_date = models.DateTimeField()
  price = models.DecimalField(max_digits=12, decimal_places=2)
  freight_value= models.DecimalField(max_digits=12, decimal_places=2)

class OrderPayment(models.Model):
  order_uuid = models.CharField(max_length=50)
  payment_sequential = models.IntegerField()
  payment_type = models.CharField(max_length=50)
  payment_installments = models.IntegerField()
  payment_value = models.DecimalField(max_digits=12, decimal_places=2)

class OrderReview(models.Model):
  review_uuid = models.CharField(max_length=50)
  order_uuid = models.CharField(max_length=50)
  review_score= models.IntegerField()
  review_comment_title=models.TextField(default=None, blank=True, null=True)
  review_comment_message=models.TextField(default=None, blank=True, null=True)
  review_creation_date=models.DateTimeField()
  review_answer_timestamp=models.DateTimeField()

class Order(models.Model):
  order_uuid=models.CharField(max_length=50)
  customer_uuid=models.CharField(max_length=50)
  status=models.CharField(max_length=50)
  purchase_timestamp=models.DateTimeField()
  approved_at=models.DateTimeField(default=None, blank=True, null=True)
  carrier_date=models.DateTimeField(default=None, blank=True, null=True)
  delivered_customer_date=models.DateTimeField(default=None, blank=True, null=True)
  estimated_delivery_date=models.DateTimeField()

class Product(models.Model):
  product_uuid=models.CharField(max_length=50)
  category_name=models.CharField(max_length=50)
  name_length=models.IntegerField(default=None, blank=True, null=True)
  description_length=models.IntegerField(default=None, blank=True, null=True)
  photos_count=models.IntegerField(default=None, blank=True, null=True)
  weight_in_grams=models.FloatField(default=None, blank=True, null=True)
  length_in_cm=models.FloatField(default=None, blank=True, null=True)
  height_in_cm=models.FloatField(default=None, blank=True, null=True)
  width_in_cm=models.FloatField(default=None, blank=True, null=True)

class Seller(models.Model):
  seller_uuid=models.CharField(max_length=50)
  zip_code_prefix=models.CharField(max_length=12)
  city=models.CharField(max_length=50)
  state=models.CharField(max_length=30)

class CategoryNameTranslation(models.Model):
  category_name=models.CharField(max_length=200)
  category_name_english=models.CharField(max_length=200)

class SellerUser(models.Model):
  seller_uuid=models.CharField(max_length=50)
  user_id=models.IntegerField()

class CustomerUser(models.Model):
  customer_unique_id=models.CharField(max_length=50)
  user_id=models.IntegerField()

# This model is intended to represent
# seller records regarding what they already
# have in their inventory, and what is available
# for them to buy.  there should be no records
# that are neither owned nor available, and
# owned/available should be mutually exclusive.
# Down the line we can use these along with statistical
# information from recent orders to optimize purchasing.
class InventoryItem(models.Model):
  seller_uuid=models.CharField(max_length=50)
  product_uuid=models.CharField(max_length=50)
  name=models.CharField(max_length=100)
  owned=models.BooleanField()
  available=models.BooleanField()
  wholesale_unit_price=models.DecimalField(max_digits=12, decimal_places=2)
  count=models.IntegerField()

  @property
  def inventory_status(self):
    if self.owned:
      return "OWNED"
    elif self.available:
      return "AVAILABLE"
    else:
      raise RuntimeError("Invalid Inventory State")

class MerchantRanking(models.Model):
  seller_id=models.IntegerField(primary_key=True)
  review_count=models.IntegerField()
  mean_score=models.FloatField()

  @property
  def formated_rank(self):
    return "{:.2f}".format(self.mean_score)

  class Meta:
    managed = False
    db_table = 'merchant_ranking'