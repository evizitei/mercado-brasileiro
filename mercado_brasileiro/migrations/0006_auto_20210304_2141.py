# Generated by Django 3.1.6 on 2021-03-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado_brasileiro', '0005_orderreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderreview',
            name='review_comment_message',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='orderreview',
            name='review_comment_title',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]