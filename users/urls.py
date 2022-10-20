
from django.urls import path
 # importing views from views..py
from .views import BookDetail, OverduepaymentList,StudentDetail,BorrowedDetail,AssignedBooks,IssuingBook,AllBooksDetail,Overduepayment,OverduepaymentList,AuditReportList,MyObtainTokenPairView,RegisterView,DuePayment,LoginView\
                   ,BookDetailView,Register,DetailedStudentView,ReturnBookView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('student_list/', StudentDetail.as_view({'get':'list'}),name='student_list'),
    path('student_detail/<str:pk>/', StudentDetail.as_view({'get':'retrieve','put':'update','delete':'destroy'}),name='student_detail'),
    path('book_list/', BookDetail.as_view({'get':'list','post':'create'}),name='book_list'),
    path('book_detail/<int:pk>/', BookDetail.as_view({'get':'retrieve','put':'update','delete':'destroy'}),name='book_detail'),
    path('borrowed_books_detail/', BorrowedDetail.as_view({'get':'list'}),name='books_borrowed'),
    path('student_books/<int:pk>/<str:books>/', AssignedBooks.as_view(),name='assigned_books'),
    path('borrower_entry/', AllBooksDetail.as_view(),name='available_data'),
    path('borrower_entry/<int:pk>/', IssuingBook.as_view(),name='return_book'),
    path('overdue_list/', OverduepaymentList.as_view(),name='overdue_list'),
    path('overdue_list/<int:pk>/', Overduepayment.as_view(),name='overdue_detail'),
    path('overdue_list/<int:student>/<int:book>/', Overduepayment.as_view(),name='overdue_payment'),
    path('audit_report/', AuditReportList.as_view(),name='audit_detail'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('duepayment/<int:student>/', DuePayment.as_view(),name='audit_detail'),
    path('loginview/', LoginView.as_view(),name='loginview'),
    path('bookview/', BookDetailView.as_view(),name='BookDetailView'),
    path('register_user/', Register.as_view(),name='Register'),
    path('student_detail_view/', DetailedStudentView.as_view(),name='Register'),
    path('return_book/', ReturnBookView.as_view(),name='return'),
    
    
    
]   