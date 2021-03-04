import csv
import environ
import os
import psycopg2
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


from mercado_brasileiro.models import Customer
from mercado_brasileiro.models import GeoLocation
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

import_customers()
import_geolocations()


print("Script Complete")