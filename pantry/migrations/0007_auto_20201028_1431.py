# Generated by Django 3.1.2 on 2020-10-28 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0006_auto_20201028_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='prod_quantity',
            field=models.IntegerField(default=0),
        ),
    ]