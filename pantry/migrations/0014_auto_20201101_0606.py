# Generated by Django 3.1.2 on 2020-11-01 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0013_auto_20201031_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_quantity',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]