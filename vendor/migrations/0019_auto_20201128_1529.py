# Generated by Django 3.1.2 on 2020-11-28 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0018_userdetails_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ),
    ]
