# Generated by Django 4.1.7 on 2023-04-18 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewrating",
            name="rating",
            field=models.FloatField(
                choices=[
                    (1, "1 star"),
                    (2, "2 star"),
                    (3, "3 star"),
                    (4, "4 star"),
                    (5, "5 star"),
                ]
            ),
        ),
    ]
