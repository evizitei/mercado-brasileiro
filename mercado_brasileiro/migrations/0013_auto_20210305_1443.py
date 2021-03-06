# Generated by Django 3.1.6 on 2021-03-05 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado_brasileiro', '0012_auto_20210305_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='height_in_cm',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='length_in_cm',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_in_grams',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='width_in_cm',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
