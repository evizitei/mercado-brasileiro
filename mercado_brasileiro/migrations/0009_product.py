# Generated by Django 3.1.6 on 2021-03-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado_brasileiro', '0008_auto_20210305_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_uuid', models.CharField(max_length=50)),
                ('category_name', models.CharField(max_length=50)),
                ('name_length', models.IntegerField()),
                ('description_length', models.IntegerField()),
                ('photos_count', models.IntegerField()),
                ('weight_in_grams', models.FloatField()),
                ('length_in_cm', models.FloatField()),
                ('height_in_cm', models.FloatField()),
                ('width_in_cm', models.FloatField()),
            ],
        ),
    ]