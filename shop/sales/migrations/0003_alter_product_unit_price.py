# Generated by Django 4.2.8 on 2023-12-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.FloatField(default=0),
        ),
    ]
