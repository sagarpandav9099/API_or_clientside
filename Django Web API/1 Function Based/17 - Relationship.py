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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

@api_view(['GET', 'POST'])
def author_list(request):
    """
    List all authors, or create a new author.
    """
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):
    """
    Retrieve, update or delete an author by ID.
    """
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def book_list(request):
    """
    List all books, or create a new book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    """
    Retrieve, update or delete a book by ID.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author-list'),
    path('authors/<int:pk>/', views.author_detail, name='author-detail'),
    path('books/', views.book_list, name='book-list'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
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