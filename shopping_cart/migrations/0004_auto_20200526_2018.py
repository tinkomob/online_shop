# Generated by Django 2.2.10 on 2020-05-26 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0003_auto_20200526_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
