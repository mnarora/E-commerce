# Generated by Django 3.1.2 on 2020-10-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0004_auto_20201025_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='pantry/images'),
        ),
    ]
