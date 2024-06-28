# Generated by Django 4.1.13 on 2024-06-25 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthData', '0007_customuser_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type_user',
            field=models.CharField(choices=[('profissional', 'Profissional'), ('paciente', 'Paciente'), ('admin', 'Admin')], default='profissional', max_length=255),
        ),
    ]
