# Generated by Django 4.1.1 on 2022-10-07 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuditReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrower', models.CharField(max_length=50)),
                ('total_amount_overdued', models.IntegerField(default=0)),
                ('borrowed_year', models.IntegerField()),
                ('book', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Book_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=0, max_length=200)),
                ('publication_year', models.DateTimeField()),
                ('language', models.CharField(max_length=200)),
                ('no_of_copies_actual', models.IntegerField(blank=True, null=True)),
                ('no_of_copies_current', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sex', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='M', max_length=5)),
                ('date_of_birth', models.DateTimeField()),
                ('department', models.CharField(choices=[('ENGINEERING', 'ENGINEERING'), ('COMMERCE', 'COMMERCE'), ('ARTS', 'ARTS')], max_length=20)),
                ('contact_number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='staff_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField()),
                ('designation', models.CharField(choices=[('ASSOCIATE_LIBRARIAN', 'ASSOCIATE'), (',SENIOR_LIBRARIAN', 'SENIOR'), ('JUNIOR_LIBRARIAN', 'JUNIOR')], default='JUNIOR', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Borrower_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
                ('actual_return_date', models.DateTimeField(blank=True, null=True)),
                ('remained_days_return', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('ASSIGNED', 'ASSIGNED'), ('RETURNED', 'RETURNED')], default='ASSIGNED', max_length=12)),
                ('overdue_amount', models.IntegerField(default=0)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book', to='users.book_details')),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='users.student_details')),
                ('issued_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_by', to='users.staff_details')),
            ],
        ),
        migrations.AddField(
            model_name='book_details',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='users.category_details'),
        ),
    ]
