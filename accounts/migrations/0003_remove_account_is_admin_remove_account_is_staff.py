# Generated by Django 4.1.7 on 2023-04-18 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_account_phone_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="is_admin",
        ),
        migrations.RemoveField(
            model_name="account",
            name="is_staff",
        ),
    ]
