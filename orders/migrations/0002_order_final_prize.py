# Generated by Django 4.1.7 on 2023-05-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="final_prize",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]