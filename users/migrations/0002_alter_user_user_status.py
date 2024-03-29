# Generated by Django 5.0.1 on 2024-02-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.CharField(choices=[('new', 'new'), ('code_verified', 'code_verified'), ('done', 'done')], default='new', max_length=31),
        ),
    ]
