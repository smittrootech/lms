# Generated by Django 4.1.1 on 2022-10-07 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.CharField(choices=[('Student', 'Student'), ('Admin', 'Admin'), ('Superuser', 'Superuser')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
