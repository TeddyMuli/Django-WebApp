# Generated by Django 4.2 on 2023-05-18 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_debt_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='paid_debt',
        ),
    ]
