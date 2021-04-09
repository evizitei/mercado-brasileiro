# Generated by Django 3.1.6 on 2021-04-09 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado_brasileiro', '0024_inventory_value_trigger'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPredictedSatisfaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_uuid', models.CharField(max_length=50)),
                ('customer_uuid', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('purchase_timestamp', models.DateTimeField()),
                ('approved_at', models.DateTimeField()),
                ('carrier_date', models.DateTimeField()),
                ('delivered_customer_date', models.DateTimeField()),
                ('estimated_delivery_date', models.DateTimeField()),
                ('predicted_satisfaction', models.IntegerField()),
                ('seller_uuid', models.CharField(max_length=50)),
            ],
        ),
    ]
