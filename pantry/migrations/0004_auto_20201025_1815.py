# Generated by Django 3.1.2 on 2020-10-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0003_auto_20201025_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(default='', max_length=300),
        ),
    ]
