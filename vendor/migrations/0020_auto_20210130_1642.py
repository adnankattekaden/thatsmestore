# Generated by Django 2.2.12 on 2021-01-30 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0019_auto_20201128_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
