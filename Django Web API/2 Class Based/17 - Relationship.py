# API Project
# -----------

# TODO Create Project for API

python -m venv myenv
myenv\Scripts\activate
pip install django   
python -m pip install --upgrade pip
django-admin startproject ECommerce .
python manage.py startapp master
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
admin
admin@gmail.com
password
password
y
pip install djangorestframework     
python manage.py runserver


# TODO Install Apps in setting.py

'rest_framework',
'master',


# TODO Create Model
# master/models.py

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'summary', 'author']


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'books']



# TODO Create view
# master/views.py

from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing author instances.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer



# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('master.urls')),  # Include the master app URLs
]



# TODO Test api in postman
# ? 1. Create a New Author (POST)
# URL: http://127.0.0.1:8000/api/authors/
# Method: POST

{
    "name": "George Orwell",
    "biography": "George Orwell was an English novelist, essayist, journalist and critic."
}

# Expected Response:

{
    "id": 1,
    "name": "George Orwell",
    "biography": "George Orwell was an English novelist, essayist, journalist and critic.",
    "books": []
}

# ? 2. Create a New Book (POST)
# URL: http://127.0.0.1:8000/api/books/
# Method: POST

{
    "title": "1984",
    "summary": "A dystopian social science fiction novel and cautionary tale.",
    "author": 1
}

# Expected Response:

{
    "id": 1,
    "title": "1984",
    "summary": "A dystopian social science fiction novel and cautionary tale.",
    "author": 1
}

# ? 3. List All Authors with Nested Books (GET)
# URL: http://127.0.0.1:8000/api/authors/
# Method: GET
# Description: Retrieves a list of all authors with their nested books.
# Example Response:

[
    {
        "id": 1,
        "name": "George Orwell",
        "biography": "George Orwell was an English novelist, essayist, journalist and critic.",
        "books": [
            {
                "id": 1,
                "title": "1984",
                "summary": "A dystopian social science fiction novel and cautionary tale.",
                "author": 1
            }
        ]
    }
]

# ? 4. Retrieve Author by ID with Nested Books (GET)
# URL: http://127.0.0.1:8000/api/authors/1/
# Method: GET
# Description: Retrieves the details of the author with ID 1, including nested books.
# Example Response:

{
    "id": 1,
    "name": "George Orwell",
    "biography": "George Orwell was an English novelist, essayist, journalist and critic.",
    "books": [
        {
            "id": 1,
            "title": "1984",
            "summary": "A dystopian social science fiction novel and cautionary tale.",
            "author": 1
        }
    ]
}

# ? 5. List All Books (GET)
# URL: http://127.0.0.1:8000/api/books/
# Method: GET
# Description: Retrieves a list of all books.
# Example Response:

[
    {
        "id": 1,
        "title": "1984",
        "summary": "A dystopian social science fiction novel and cautionary tale.",
        "author": 1
    }
]