# Generated by Django 4.1.1 on 2022-10-10 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
    ]
