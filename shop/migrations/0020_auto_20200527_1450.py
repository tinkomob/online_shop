# Generated by Django 2.2.10 on 2020-05-27 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
