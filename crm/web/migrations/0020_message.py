# Generated by Django 4.2 on 2023-05-29 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_remove_record_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]