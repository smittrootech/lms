# Generated by Django 4.1.1 on 2022-10-10 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_book_details_publication_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_details',
            name='publication_year',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]