# Generated by Django 4.1.7 on 2023-04-22 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0002_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="cart_id",
        ),
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
