# Generated by Django 4.1.7 on 2023-05-07 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_final_prize"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="final_prize",
        ),
    ]
