# Generated by Django 4.1.7 on 2023-08-24 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0009_payment_updated_at"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Refund",
        ),
    ]
