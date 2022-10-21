from calendar import c
from django.shortcuts import get_object_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from users.permission import ReadOnly
from .models import AuditReport,Borrower_Details,Book_Details,AuditReport,Duepayment
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .serializers import BookDetailsSerializers, DuePaymentSerializer,IssuingbookSerialzer, PaymentSerializer,StudentsbookSerialzer,AuditReportSerializer
from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from base import Constants
from .models import User
from .serializers import MyTokenObtainPairSerializer,RegisterSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Sum
from django.views.generic import TemplateView,ListView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class StudentDetail(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAdminUser|ReadOnly]
    
    def list(self, request):
        queryset = User.objects.filter(is_staff=False)
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, email=pk)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        serializer = RegisterSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(TemplateView):
    template_name = "users/login.html"

class BookDetailView(TemplateView):
    template_name = "users/books.html"

    def get_context_data(self,*args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args,**kwargs)
        staff=User.objects.filter(is_staff=True)
        print(self.request.user.id)
        context['user']=[i.email for i in staff]
        return context

class Register(TemplateView):
    template_name = "users/user_registration.html"

class DetailedStudentView(TemplateView):
    template_name = "users/assign_book.html"

class ReturnBookView(TemplateView):
    template_name = "users/return_book.html"

# class BaseViewSet(TemplateView):

#     template_name ="users/base.html"

#     def get_context_data(self,*args, **kwargs):
#         context = super(BaseViewSet, self).get_context_data(*args,**kwargs)
#         print(self.request.user)
#         return context



class LogoutView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        # try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


class BookDetail(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAdminUser|ReadOnly]

    def list(self, request):
        queryset = Book_Details.objects.all()
        serializer = BookDetailsSerializers(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # queryset = Book_Details.objects.all()
        # user = get_object_or_404(queryset)
        # print(request.data)
        serializer = BookDetailsSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        print(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book_Details.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookDetailsSerializers(user)
        return Response(serializer.data)
    
    def update(self, request, pk):
        queryset = Book_Details.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        print(request.data)
        serializer = BookDetailsSerializers(user,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = Book_Details.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowedDetail(viewsets.ViewSet):

    permission_classes = [IsAdminUser|ReadOnly]

    def list(self, request):
        queryset = Borrower_Details.objects.all()
        serializer = StudentsbookSerialzer(queryset, many=True)
        return Response(serializer.data)


class AssignedBooks(APIView): 

    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self,pk,book):
        try:
            return Borrower_Details.objects.filter(pk=pk)
        except Borrower_Details.DoesNotExist:
            raise Http404

    def get(self,request,pk, format=None):
        queryset = self.get_object(pk,None)
        serializer = StudentsbookSerialzer(queryset,many=True)
        return Response(serializer.data)



class AssignedBooks(APIView): 

    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self,pk,books):
        try:
            print(Borrower_Details.objects.filter(id=pk).filter(book__title=books))
            return Borrower_Details.objects.filter(id=pk).filter(book__title=books)
        except Borrower_Details.DoesNotExist:
            raise Http404

    def get(self,request,pk,books):
        try:
            queryset=self.get_object(pk,books)
            serializer = StudentsbookSerialzer(queryset,many=True)
            return Response(serializer.data)
        except Borrower_Details.DoesNotExist:
            raise Http404
            
    def put(self,request,pk,books):        
        queryset=self.get_object(pk,books).first()
        serializer = StudentsbookSerialzer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllBooksDetail(APIView):

    permission_classes = [IsAdminUser|ReadOnly]

    def get(self, request, format=None):
        queryset = Borrower_Details.objects.all()
        serializer = IssuingbookSerialzer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):

        book = Book_Details.objects.filter(id=request.data['book'], no_of_copies_current__gt=0)
        if not book.exists():
            return Response({"error":"Book is not available"}, status=status.HTTP_400_BAD_REQUEST)
        
        find_due=Borrower_Details.objects.filter(
            borrower= User.objects.get(id=request.data['borrower']),
            overdue_amount__gt=0,
            status=Borrower_Details.Status.ASSIGNED.name
        )
           
        if find_due.exists():
            string=""
            for index,overdued_books in enumerate(find_due):
                book_name=find_due[index].book.title
                amount=find_due[index].overdue_amount
                string=string+","+f"{book_name} is overdued with {amount} rs."
            return Response({"error":f"Overdued books"}, status=status.HTTP_400_BAD_REQUEST)

        borrower_obj = Borrower_Details.objects.filter(
            borrower= User.objects.get(id=request.data['borrower']),\
            book = book.first(),
            status=Borrower_Details.Status.ASSIGNED.name
        )
        
        if borrower_obj.exists():
                #raise serializers.ValidationError({"detail":"Object Exixts."})
                return Response({"error":"Object Exixts."}, status=status.HTTP_400_BAD_REQUEST)

        queryset_borr = Borrower_Details.objects.filter( \
                                                borrower__id=request.data['borrower'], \
                                                status = Borrower_Details.Status.ASSIGNED.name
                                                )
        if queryset_borr.exists():
            if queryset_borr.count() == Constants.data.get('NO_BOOKS_AVAILED_BY_STUDENT'):
                raise serializers.ValidationError({"detail":"User can not be assigned 4th book. Please return one book to borrow new"})
        avil_books=Book_Details.objects.filter(id = request.data['book']).first().no_of_copies_current
        Book_Details.objects.filter(id = request.data['book']).update(no_of_copies_current= avil_books-1)
        serializer = IssuingbookSerialzer(context = {'request':request},data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer['book'].no_of_copies_current=serializer['book'].no_of_copies_current-1
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssuingBook(APIView):

    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self,pk):
        try:
            return Borrower_Details.objects.filter(borrower__id=pk,status=Borrower_Details.Status.ASSIGNED.name )
        except Borrower_Details.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        try:
            queryset=self.get_object(pk)
            serializer = IssuingbookSerialzer(queryset,many=True)
            return Response(serializer.data)
        except Borrower_Details.DoesNotExist:
            raise Http404


    def put(self,request,pk):        
        queryset=self.get_object(pk).first()
        serializer = IssuingbookSerialzer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OverduepaymentList(APIView):

    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self):
        try:
            return Borrower_Details.objects.filter(overdue_amount__gt=0)
        except Borrower_Details.DoesNotExist:
            raise Http404
    
    def get(self,request):
        try:
            queryset=self.get_object()
            serializer = PaymentSerializer(queryset,many=True)
            return Response(serializer.data)
        except Borrower_Details.DoesNotExist:
            raise Http404

class Overduepayment(APIView):

    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self,pk):
        try:
            return Borrower_Details.objects.filter(borrower__id=pk,overdue_amount__gt=0)
        except Borrower_Details.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        try:
            queryset=self.get_object(pk)
            serializer = PaymentSerializer(queryset,many=True)
            return Response(serializer.data)
        except Borrower_Details.DoesNotExist:
            raise Http404

    def put(self,request,student,book):      
        queryset=Borrower_Details.objects.filter(borrower__id=student,book__id=book,overdue_amount__gt=0).first()
        # audit_report=AuditReport(borrower=queryset.borrower.email,total_amount_overdued=queryset.overdue_amount,borrowed_year=timezone.now().year,book=queryset.book.title)
        # audit_report.save()
        serializer = PaymentSerializer(queryset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuditReportList(generics.ListCreateAPIView):
 
    permission_classes = [IsAdminUser|ReadOnly]

    queryset = AuditReport.objects.all()

    serializer_class = AuditReportSerializer

class DuePayment(generics.ListCreateAPIView):
 
    permission_classes = [IsAdminUser|ReadOnly]

    def get_object(self,request,student):
        try:
            return  Borrower_Details.objects.filter(borrower=student,overdue_amount__gt=0)
            # return Borrower_Details.objects.filter(borrower=student,overdue_amount__gt=0).aggregate(Sum('overdue_amount'))
        except Borrower_Details.DoesNotExist:
            raise Http404

    def get(self,request,student):
        try:
            queryset=self.get_object(request,student)
            serializer = DuePaymentSerializer(queryset)
            return Response(serializer.data)
        except Borrower_Details.DoesNotExist:
            raise Http404


@api_view(('POST',))
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    # from_email = request.POST.get('from_email', '')

    to_email = request.POST.getlist('to_email', '')
    to_email=list(to_email)
    if subject and message and to_email:
        try:
            send_mail(subject, message, 'smitkumar.patel@trootech,com', to_email)
        except BadHeaderError:
            return Response({"detail":'Invalid header found.'})
        return Response({"detail":"mail sent"})
    else:
        return Response({"detail":'Make sure all fields are entered and valid.'})