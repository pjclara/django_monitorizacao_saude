# Generated by Django 4.1.13 on 2024-06-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthData', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
