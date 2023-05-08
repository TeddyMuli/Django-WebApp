# Generated by Django 4.2 on 2023-04-25 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('phone_no', models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]