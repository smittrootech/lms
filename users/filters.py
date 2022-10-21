from .models import Book_Details

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = Book_Details
        fields = {
            'book': ['exact', 'contains']
        }

