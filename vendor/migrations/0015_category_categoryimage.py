# Generated by Django 3.1.2 on 2020-11-24 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0014_auto_20201124_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='categoryimage',
            field=models.ImageField(blank=True, null=True, upload_to='category/images'),
        ),
    ]
