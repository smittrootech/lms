# Generated by Django 4.1.1 on 2022-10-19 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_remove_duepayment_overdue_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='duepayment',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_detail', to='users.book_details'),
        ),
    ]
