# Generated by Django 4.2 on 2023-05-17 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_sale_paid_alter_sale_pay_alter_sale_product_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Debt',
        ),
    ]
