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

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# OR

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['id', 'first_name', 'last_name', 'email', 'department']


# TODO Create view
# master/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['GET'])
def filter_employees(request):
    filters = {}
    # Extract query parameters for filtering
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    email = request.GET.get('email', None)
    department = request.GET.get('department', None)

    # Apply filters if parameters are present
    if first_name:
        filters['first_name__icontains'] = first_name
    if last_name:
        filters['last_name__icontains'] = last_name
    if email:
        filters['email__icontains'] = email
    if department:
        filters['department__icontains'] = department

    employees = Employee.objects.filter(**filters)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.filter_employees, name='filter_employees'),
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('master.urls')),  # Include the employee app URLs
]


# TODO Test api in postman
# ? 1. Get all filtered employees
# Method: GET
# URLs: 
# http://127.0.0.1:8000/api/employees/?first_name=John
# http://127.0.0.1:8000/api/employees/?last_name=Smith
# http://127.0.0.1:8000/api/employees/?email=alice
# http://127.0.0.1:8000/api/employees/?department=Engineering
# http://127.0.0.1:8000/api/employees/?first_name=Charlie&department=Engineering
# http://127.0.0.1:8000/api/employees/?first_name=Alice&last_name=Johnson&department=Engineering
# http://127.0.0.1:8000/api/employees/?email=doe&department=Engineering

