# Generated by Django 3.1.2 on 2020-11-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0009_shippingaddress_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
