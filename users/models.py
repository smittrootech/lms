import email
from email.policy import default
from math import floor
from random import choices
from secrets import choice
from typing_extensions import Required
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
from pkg_resources import require
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from base import Constants
# from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models

from django.contrib.auth.models import AbstractUser,BaseUserManager



# #################################################
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('roles', User.Role.Admin.name)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    class Role(models.TextChoices):
        Student = 'Student', _('Student')
        Admin = 'Admin', _('Admin')

    class Gender(models.TextChoices):
        Male = 'M', _('Male')
        Female = 'F', _('Female')

    class StudentDept(models.TextChoices):
        ENGINEERING = 'ENGINEERING', _('ENGINEERING')
        COMMERCE = 'COMMERCE', _('COMMERCE')
        ARTS = 'ARTS', _('ARTS')


        
    username=None
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    roles = models.CharField(max_length=50, choices = Role.choices)
    sex=models.CharField(max_length=5,choices=Gender.choices,)
    department=models.CharField(max_length=20,choices=StudentDept.choices)
    contact_number=models.IntegerField(default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Category_Details(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book_Details(models.Model):
    title=models.CharField(max_length=200,default=0)
    publication_year=models.DateField(null=True,blank=True)
    language=models.CharField(max_length=200)
    category=models.ForeignKey(Category_Details,on_delete=models.CASCADE,related_name='category', blank=True, null=True)
    no_of_copies_actual=models.IntegerField(blank=True,null=True)
    no_of_copies_current=models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.title


class Borrower_Details(models.Model):

    class Status(models.TextChoices):
        ASSIGNED = 'ASSIGNED', _('ASSIGNED')
        RETURNED = 'RETURNED', _('RETURNED')
        
    borrower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='student', blank=True, null=True)
    book=models.ForeignKey(Book_Details,on_delete=models.CASCADE,related_name='book', blank=True, null=True)
    from_date=models.DateTimeField(null=True,blank=True)
    to_date=models.DateTimeField(null=True,blank=True)
    actual_return_date=models.DateTimeField(null=True,blank=True)
    remained_days_return=models.IntegerField(default=0)
    issued_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='issued_by', blank=True,null=True)
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.ASSIGNED.name)
    overdue_amount=models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if self.status==self.Status.RETURNED:
            self.actual_return_date=timezone.now()
            self.overdue_amount=0

        if self.actual_return_date:
            if self.actual_return_date > self.to_date and self.status!=self.Status.RETURNED:
                self.remained_days_return=(self.to_date-self.actual_return_date).days
                 

        elif self.to_date:
            self.remained_days_return=(self.to_date-timezone.now()).days + 1

        if self.remained_days_return <-1 and not self.actual_return_date:
            self.overdue_amount=abs(self.remained_days_return*Constants.data.get('OVERDUE_AMOUNT'))
        
        
        return super().save(*args, **kwargs)  

class AuditReport(models.Model):
    borrower=models.CharField(max_length=50)
    total_amount_overdued=models.IntegerField(default=0)
    borrowed_year=models.IntegerField()
    book=models.CharField(max_length=30)

class Duepayment(models.Model):
    borrower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrower_detail', blank=True, null=True)
    amount_to_be_paid=models.IntegerField(default=0)
 