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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from django.db.models import Q
from .models import Teacher
from .serializers import TeacherSerializer

@api_view(['GET'])
def teacher_list(request):
    """
    List all teachers with filtering, searching, and ordering.
    """
    queryset = Teacher.objects.all()

    # Filter by subject and city
    subject = request.GET.get('subject', None)
    city = request.GET.get('city', None)

    if subject:
        queryset = queryset.filter(subject=subject)
    if city:
        queryset = queryset.filter(city=city)

    # Search across multiple fields
    search_query = request.GET.get('search', None)
    if search_query:
        queryset = queryset.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    # Ordering
    ordering = request.GET.get('ordering', None)
    if ordering:
        queryset = queryset.order_by(ordering)

    # Serialize the data
    serializer = TeacherSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import teacher_list

urlpatterns = [
    path('teachers/', teacher_list, name='teacher-list'),
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