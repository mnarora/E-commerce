# Generated by Django 3.1.2 on 2020-11-01 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_cost', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_success', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_amount', models.IntegerField(default=0)),
                ('order_address', models.CharField(default='', max_length=500)),
                ('order_city', models.CharField(default='', max_length=50)),
                ('order_state', models.CharField(default='', max_length=50)),
                ('order_phone', models.BigIntegerField(default=0)),
                ('shipped', models.BooleanField(default=False)),
                ('deliverred', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=30)),
                ('category', models.CharField(default='', max_length=300)),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(default='', upload_to='pantry/images')),
                ('availability', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.product')),
                ('wishlist_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.wishlist')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.CharField(default='', max_length=300)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order_quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.order')),
                ('p_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.order')),
                ('p_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_quantity', models.IntegerField(default=0)),
                ('cart_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.cart')),
                ('p_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pantry.product')),
            ],
        ),
    ]
