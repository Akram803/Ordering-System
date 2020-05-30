# Generated by Django 3.0.4 on 2020-05-06 19:26

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
            name='AnonymouseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=300)),
                ('checked_out', models.BooleanField(default=False)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'db_table': 'order_anonymouseorder',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_out', models.BooleanField(default=False)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order_customerorder',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField(max_length=300)),
                ('price', models.FloatField(default=0.0)),
                ('availability', models.BooleanField(default=True)),
                ('quantity', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerorderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='menu.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.CustomerOrder')),
            ],
            options={
                'db_table': 'order_customerorder_items',
                'unique_together': {('order', 'item')},
            },
        ),
        migrations.AddField(
            model_name='customerorder',
            name='items',
            field=models.ManyToManyField(through='menu.CustomerorderItems', to='menu.Item'),
        ),
        migrations.CreateModel(
            name='AnonymouseOrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('anonymouseorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.AnonymouseOrder')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='menu.Item')),
            ],
            options={
                'db_table': 'order_anonymouseorder_items',
                'unique_together': {('anonymouseorder', 'item')},
            },
        ),
        migrations.AddField(
            model_name='anonymouseorder',
            name='items',
            field=models.ManyToManyField(through='menu.AnonymouseOrderItems', to='menu.Item'),
        ),
    ]