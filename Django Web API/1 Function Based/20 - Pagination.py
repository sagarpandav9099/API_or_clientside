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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5  # You can adjust the number of items per page
}


# TODO Create Model
# master/models.py

from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.name

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# TODO Create view
# master/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Department
from .serializers import DepartmentSerializer

@api_view(['GET'])
def department_list(request):
    """
    List all departments with pagination.
    """
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of items per page
    queryset = Department.objects.all()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = DepartmentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import department_list

urlpatterns = [
    path('departments/', department_list, name='department-list'),
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
# ? 1. List All Departments with Pagination (GET)
# URL: http://127.0.0.1:8000/api/departments/
# Method: GET
# Description: Retrieves a paginated list of all departments. By default, 5 items per page.
# Example Response:

{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/departments/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Human Resources",
            "code": "HR",
            "description": "Handles employee-related services."
        },
        {
            "id": 2,
            "name": "Finance",
            "code": "FIN",
            "description": "Manages the company's finances."
        },
        {
            "id": 3,
            "name": "IT Services",
            "code": "IT",
            "description": "Provides IT support and services."
        },
        {
            "id": 4,
            "name": "Marketing",
            "code": "MKT",
            "description": "Responsible for marketing strategies."
        },
        {
            "id": 5,
            "name": "Sales",
            "code": "SAL",
            "description": "Handles sales operations and client relations."
        }
    ]
}

# ? 2. List Departments on Page 2
# URL: http://127.0.0.1:8000/api/departments/?page=2
# Method: GET
# Description: Retrieves the next set of departments on page 2.
# Example Response:

{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/departments/?page=3",
    "previous": "http://127.0.0.1:8000/api/departments/",
    "results": [
        {
            "id": 6,
            "name": "Customer Support",
            "code": "CS",
            "description": "Provides support to customers."
        },
        {
            "id": 7,
            "name": "Research and Development",
            "code": "R&D",
            "description": "Innovates and develops new products."
        },
        {
            "id": 8,
            "name": "Procurement",
            "code": "PRC",
            "description": "Manages purchasing and supplies."
        },
        {
            "id": 9,
            "name": "Logistics",
            "code": "LOG",
            "description": "Handles distribution and logistics."
        },
        {
            "id": 10,
            "name": "Production",
            "code": "PRD",
            "description": "Oversees production processes."
        }
    ]
}