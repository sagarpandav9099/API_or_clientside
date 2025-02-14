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


# TODO Install Filter Package
pip install django-filter


# TODO Install Apps in setting.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
    'master',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}


# TODO Create Model
# master/models.py

from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


# TODO Create view
# master/views.py

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherListView(generics.ListAPIView):
    """
    List all teachers with filtering, searching, and ordering.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'city']
    search_fields = ['first_name', 'last_name', 'subject', 'city']
    ordering_fields = ['first_name', 'last_name', 'email', 'subject', 'city']
    ordering = ['first_name']  # Default ordering by first name


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import TeacherListView

urlpatterns = [
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
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
# ? 1. List All Teachers Ordered by Last Name
# URL: http://127.0.0.1:8000/api/teachers/?ordering=last_name
# Method: GET
# Description: Retrieves a list of all teachers ordered by their last name.
# Example Response:

[
    {
        "id": 2,
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob.smith@example.com",
        "subject": "Physics",
        "city": "Los Angeles"
    },
    {
        "id": 1,
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "subject": "Mathematics",
        "city": "New York"
    }
]

# ? 2. Order Teachers by Email
# URL: http://127.0.0.1:8000/api/teachers/?ordering=email
# Method: GET
# Description: Retrieves a list of all teachers ordered by their email addresses.
# Example Response:

[
    {
        "id": 1,
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "subject": "Mathematics",
        "city": "New York"
    },
    {
        "id": 2,
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob.smith@example.com",
        "subject": "Physics",
        "city": "Los Angeles"
    }
]

# ? 3. Order Teachers by City Descending
# URL: http://127.0.0.1:8000/api/teachers/?ordering=-city
# Method: GET
# Description: Retrieves a list of all teachers ordered by city in descending order.
# Example Response:

[
    {
        "id": 2,
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob.smith@example.com",
        "subject": "Physics",
        "city": "Los Angeles"
    },
    {
        "id": 1,
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "subject": "Mathematics",
        "city": "New York"
    }
]