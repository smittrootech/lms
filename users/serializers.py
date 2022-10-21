from datetime import datetime,timedelta
from unicodedata import category
from venv import create
from xml.dom import ValidationErr
from rest_framework import serializers
from .models import  Book_Details,Borrower_Details,AuditReport,Duepayment
from django.utils import timezone
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# from django.contrib.auth import get_user_model
# # User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    sex = serializers.CharField(write_only=True, required=True)
    department = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','sex','department','contact_number','password', 'password2' )


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            roles=User.Role.Student.name,
            sex=validated_data['sex'],
            department=validated_data['department'],
            contact_number=validated_data['contact_number']
        )
   
    
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
         return super().update(instance, validated_data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.email
        return token


class BookDetailsSerializers(serializers.ModelSerializer):
    # publication_year=serializers.DateField(write_only=True)
    # language= serializers.CharField(max_length=50,write_only=True)
    # category= serializers.CharField(max_length=50,write_only=True)

    
    class Meta:
        model = Book_Details
        fields = ['id','title','no_of_copies_actual','no_of_copies_current','publication_year','language','category']

class BorrowerSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Borrower_Details
        fields = '__all__'

class StudentsbookSerialzer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()

    def get_book(self,object):
        if object:
            return object.book.title

    def get_student(self,object):
        if object:
            return object.borrower.email

    def update(self, instance, validated_data):
        book=Book_Details.objects.filter(title=instance.book).first()
        instance.actual_return_date = validated_data.get('actual_return_date', instance.actual_return_date)
        instance.status = validated_data.get('status', instance.status)

        if instance.status=="RETURNED":
            print("in return")
            book.no_of_copies_current=book.no_of_copies_current+1
            instance.save()
            book.save()
            return instance

        elif instance.status=="ASSIGNED":
            print("in assigned")
            book.no_of_copies_current=book.no_of_copies_current-1           
            instance.save()
            book.save()
            return instance

    class Meta:
        model = Borrower_Details
        fields = ('id','student','book','student','status','remained_days_return')


class IssuingbookSerialzer(serializers.ModelSerializer):



    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.from_date = timezone.now()
        instance.issued_by=self.context['request'].user
        instance.to_date=instance.from_date + timedelta(days=15)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        book=Book_Details.objects.filter(title=instance.book).first()
        instance.actual_return_date = validated_data.get('actual_return_date', instance.actual_return_date)
        previous_status=instance.status
        instance.status = validated_data.get('status', instance.status)
        if previous_status==Borrower_Details.Status.RETURNED.name:
            raise serializers.ValidationError({"detail":"book already returned"})
                
        elif instance.status==Borrower_Details.Status.RETURNED.name and \
            previous_status==Borrower_Details.Status.ASSIGNED.name: 
            if book.no_of_copies_current!=book.no_of_copies_actual:
                book.no_of_copies_current=book.no_of_copies_current+1
                instance.save()
                book.save()
            else:
                raise serializers.ValidationError({"detail":"All books are returned"})
        elif instance.status==Borrower_Details.Status.ASSIGNED.name:
            print("in assigned")
            book.no_of_copies_current=book.no_of_copies_current-1           
            instance.save()
            book.save()
        return super().update(instance, validated_data)
            

    class Meta:
        model = Borrower_Details
        fields=('borrower','book','status')

    
class PaymentSerializer(serializers.ModelSerializer):
    amount_paid=serializers.BooleanField(default=False,write_only=True)

    def update(self, instance, validated_data):
        book=Book_Details.objects.filter(title=instance.book.title).first()
        print(book.no_of_copies_current)
        if validated_data.get('amount_paid'):
            instance.status=Borrower_Details.Status.RETURNED.name 
            book.no_of_copies_current=book.no_of_copies_current+1
        instance.save()
        book.save()
        return instance
    class Meta:
        model = Borrower_Details
        fields = ['borrower','amount_paid']

class AuditReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AuditReport
        fields=['borrower','book','total_amount_overdued','borrowed_year']

class DuePaymentSerializer(serializers.ModelSerializer):
    
    # borrower = IssuingbookSerialzer()
    amount_to_be_paid= serializers.SerializerMethodField()
    books= serializers.SerializerMethodField()
    book_id=serializers.SerializerMethodField()

    # def get_books(self,object):
    #     queryset=Borrower_Details.objects.filter(borrower__id=,overdue_amount__gt=0).first()

    def get_books(self,object):
        if object:
            return [i.book.title for i in object]

    def get_book_id(self,object):
        if object:
            return [i.book.id for i in object]


    def get_amount_to_be_paid(self,object):
        if object:
            return sum([i.overdue_amount for i in object ])

    class Meta:
        model = Duepayment
        fields=['amount_to_be_paid','books','book_id']
