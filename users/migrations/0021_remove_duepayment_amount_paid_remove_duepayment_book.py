# Generated by Django 4.1.1 on 2022-10-11 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_remove_duepayment_borrowed_detail_duepayment_book_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duepayment',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='duepayment',
            name='book',
        ),
    ]