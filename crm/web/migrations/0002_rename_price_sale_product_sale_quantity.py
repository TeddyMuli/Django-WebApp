# Generated by Django 4.2 on 2023-05-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='price',
            new_name='product',
        ),
        migrations.AddField(
            model_name='sale',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
