# Generated by Django 3.1.2 on 2020-11-22 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0012_shippingaddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderverify',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
