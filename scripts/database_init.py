import csv
from datetime import datetime
from django.db import connection
from django.utils import timezone
from decimal import *
import environ
import os
import psycopg2
import pymongo
import sys
import zipfile

# Initialise environment variables,
# using the same ".env" file the django
# application uses to load database connection info
env = environ.Env()
base_dir = os.path.dirname(__file__) + "/../"
env_file = base_dir + "mercado_brasileiro/.env"
environ.Env.read_env(env_file)

# check for archive, and if present unzip
data_dir = base_dir + "data/"
extract_dir = data_dir + "olist"
data_archive = data_dir + "olist.zip"
if os.path.isfile(data_archive):
  print("Data archive present, unzipping...")
  with zipfile.ZipFile(data_archive, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
  print("...Done, removing archive")
  os.remove(data_archive)
else:
  print("No data archive, skipping unzip step.")

# Make sure the database exists, create if not
def get_app_db_conn():
  db_conn = psycopg2.connect(
    dbname=env('DATABASE_NAME'),
    user=env('DATABASE_USER'),
    host=env('DATABASE_HOST'),
    password=env('DATABASE_PASS')
  )
  return db_conn

def create_environment_db():
  from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
  conn = psycopg2.connect(
    user=env('DATABASE_USER'),
    host=env('DATABASE_HOST'),
    password=env('DATABASE_PASS')
  )
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()
  name_Database   = "SocialMedia"
  createQuery = f'CREATE DATABASE {env("DATABASE_NAME")};'
  cursor.execute(createQuery)
  print("...database created successfully")

db_connection = None
try:
  db_connection = get_app_db_conn()
  print("database connection succeeded!")
except psycopg2.OperationalError:
  print("db connection failed, trying to create database...")
  create_environment_db()
  db_connection = get_app_db_conn()
  print("db connection obtained!")


# Make sure database schema is current
os.system('python manage.py migrate')

# now all the data should be at "./data/olist/[files].csv"

import django
from django.conf import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mercado_brasileiro import settings as app_settings
os.environ["DJANGO_SETTINGS_MODULE"] = "mercado_brasileiro.settings"
django.setup()

# Database Import from Kaggle Dataset
from mercado_brasileiro.models import Customer
from mercado_brasileiro.models import GeoLocation
from mercado_brasileiro.models import OrderItem
from mercado_brasileiro.models import OrderPayment
from mercado_brasileiro.models import OrderReview
from mercado_brasileiro.models import Order
from mercado_brasileiro.models import Product
from mercado_brasileiro.models import Seller
from mercado_brasileiro.models import CategoryNameTranslation
from mercado_brasileiro.models import OrderPredictedSatisfaction

csv_dir = extract_dir

def import_model(model_class, filename, leading_column_name):
  if model_class.objects.count() > 0:
    print("CANNOT IMPORT ", model_class, ", TABLE ALREADY POPULATED!")
    return
  print("importing ", model_class, "...")
  with open(filename) as f:
    reader = csv.reader(f)
    row_count = 0
    for row in reader:
      if row[0] == leading_column_name:
        continue
      yield row
      row_count = row_count + 1
      if row_count % 1000 == 0:
        print("...imported ", row_count, " records...")
  print("...Done! ", model_class, " Count: ", model_class.objects.count())

def parse_datetime(string):
  if string is None or string == '':
    return None
  return timezone.make_aware(datetime.strptime(string, "%Y-%m-%d %H:%M:%S"))

def nullable_int(value):
  if value is None or value == '':
    return None
  return int(value)

def nullable_float(value):
  if value is None or value == '':
    return None
  return float(value)

def import_customers():
  for row in import_model(Customer, csv_dir + "/olist_customers_dataset.csv", "customer_id"):
    new_object = Customer(
      uuid=row[0],
      unique_id=row[1],
      zip_code_prefix=row[2],
      city=row[3],
      state=row[4]
    )
    new_object.save(force_insert=True)

def import_geolocations():
  for row in import_model(GeoLocation, csv_dir + "/olist_geolocation_dataset.csv", "geolocation_zip_code_prefix"):
    new_object = GeoLocation(
      zip_code_prefix=row[0],
      lat=float(row[1]),
      lng=float(row[2]),
      city=row[3],
      state=row[4]
    )
    new_object.save(force_insert=True)

def import_order_items():
  for row in import_model(OrderItem, csv_dir + "/olist_order_items_dataset.csv", "order_id"):
    new_object = OrderItem(
      order_uuid=row[0],
      order_item_id=int(row[1]),
      product_uuid=row[2],
      seller_uuid=row[3],
      shipping_limit_date=parse_datetime(row[4]),
      price=Decimal(row[5]),
      freight_value=Decimal(row[6])
    )
    new_object.save(force_insert=True)

def import_order_payments():
  for row in import_model(OrderPayment, csv_dir + "/olist_order_payments_dataset.csv", "order_id"):
    new_object = OrderPayment(
      order_uuid=row[0],
      payment_sequential=int(row[1]),
      payment_type=row[2],
      payment_installments=int(row[3]),
      payment_value=Decimal(row[4])
    )
    new_object.save(force_insert=True)

def import_order_reviews():
  for row in import_model(OrderReview, csv_dir + "/olist_order_reviews_dataset.csv", "review_id"):
    new_object = OrderReview(
      review_uuid=row[0],
      order_uuid=row[1],
      review_score=int(row[2]),
      review_comment_title=row[3],
      review_comment_message=row[4],
      review_creation_date=parse_datetime(row[5]),
      review_answer_timestamp=parse_datetime(row[6])
    )
    new_object.save(force_insert=True)

def import_orders():
  for row in import_model(Order, csv_dir + "/olist_orders_dataset.csv", "order_id"):
    new_object = Order(
      order_uuid=row[0],
      customer_uuid=row[1],
      status=row[2],
      purchase_timestamp=parse_datetime(row[3]),
      approved_at=parse_datetime(row[4]),
      carrier_date=parse_datetime(row[5]),
      delivered_customer_date=parse_datetime(row[6]),
      estimated_delivery_date=parse_datetime(row[7])
    )
    new_object.save(force_insert=True)

def import_products():
  for row in import_model(Product, csv_dir + "/olist_products_dataset.csv", "product_id"):
    new_object = Product(
      product_uuid=row[0],
      category_name=row[1],
      name_length=nullable_int(row[2]),
      description_length=nullable_int(row[3]),
      photos_count=nullable_int(row[4]),
      weight_in_grams=nullable_float(row[5]),
      length_in_cm=nullable_float(row[6]),
      height_in_cm=nullable_float(row[7]),
      width_in_cm=nullable_float(row[8]),
    )
    new_object.save(force_insert=True)

def import_sellers():
  for row in import_model(Seller, csv_dir + "/olist_sellers_dataset.csv", "seller_id"):
    new_object = Seller(
      seller_uuid=row[0],
      zip_code_prefix=row[1],
      city=row[2],
      state=row[3]
    )
    new_object.save(force_insert=True)

def import_category_name_translations():
  for row in import_model(CategoryNameTranslation, csv_dir + "/product_category_name_translation.csv", "product_category_name"):
    new_object = CategoryNameTranslation(
      category_name=row[0],
      category_name_english=row[1]
    )
    new_object.save(force_insert=True)

def import_order_predicted_satisfaction():
  for row in import_model(OrderPredictedSatisfaction, csv_dir + "/order_predicted_satisfaction.csv", "order_id"):
    new_object = OrderPredictedSatisfaction(
      order_uuid=row[0],
      customer_uuid=row[1],
      status=row[2],
      purchase_timestamp=parse_datetime(row[3]),
      approved_at=parse_datetime(row[4]),
      carrier_date=parse_datetime(row[5]),
      delivered_customer_date=parse_datetime(row[6]),
      estimated_delivery_date=parse_datetime(row[7]),
      predicted_satisfaction=int(float(row[8])),
      seller_uuid=row[9]
    )
    new_object.save(force_insert=True)

import_customers()
import_geolocations()
import_order_items()
import_order_payments()
import_order_reviews()
import_orders()
import_products()
import_sellers()
import_category_name_translations()
import_order_predicted_satisfaction()

print("Postgres Database Initialization Complete")

# MONGODB Initialization
query = '''SELECT customer.state AS customer_state, CAST(order_item.price AS float), seller.state AS seller_state, product.category_name  
FROM mercado_brasileiro_customer customer
JOIN mercado_brasileiro_order orders
ON customer.uuid = orders.customer_uuid
JOIN mercado_brasileiro_orderitem order_item
ON orders.order_uuid = order_item.order_uuid
JOIN mercado_brasileiro_seller seller
ON order_item.seller_uuid = seller.seller_uuid
JOIN mercado_brasileiro_product product
ON order_item.product_uuid = product.product_uuid'''

cursor = connection.cursor()
cursor.execute(query)
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
mongo_data = dictfetchall(cursor)

print("Connecting to mongodb...")
client = pymongo.MongoClient(env('MONGO_CONN_STRING'))
mdb = client[env('MONGO_DB_NAME')]
analytics_collection = mdb.analytics
if analytics_collection.count({}) > 0:
  print("...conn established.  Mongo already has records, looks fine.")
else:
  analytics_collection.insert_one({"Test": "Document"})
  print("...conn established and test document inserted!")

vis_collection = mdb['vis']
if vis_collection.count({}) > 0:
  print("...conn established.  Mongo already has records, looks fine.")
else:
  for datum in mongo_data:
    vis_collection.insert_one(datum)
  print("...conn established and all documents insterted!")

# making sure we have a SUPER user for admin
from django.contrib.auth.models import User
if User.objects.count() <= 0:
  print("creating root admin user...")
  User.objects.create_superuser(env('ROOT_ADMIN_USER_NAME'), env('ROOT_ADMIN_USER_EMAIL'), env('ROOT_ADMIN_USER_PASSWORD'))
  print("..created root admin.")
else:
  print("admin users already exist.")

print("DONE!")