# Generated by Django 4.2 on 2023-05-09 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_route'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
            ],
        ),
    ]