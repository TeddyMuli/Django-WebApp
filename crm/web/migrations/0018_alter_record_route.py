# Generated by Django 4.2 on 2023-05-10 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_record_route_record_user_delete_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='route',
            field=models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to='web.route'),
        ),
    ]