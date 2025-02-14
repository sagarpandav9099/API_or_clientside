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


# TODO Install Package for Image Upload

pip install Pillow


# TODO Install Apps in setting.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'master',
]

# Configure media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# TODO Create Model
# master/models.py

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)  # Image field
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)  # PDF file field

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeListCreateView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class DeleteAllEmployeesView(APIView):
    def delete(self, request):
        total_deleted, _ = Employee.objects.all().delete()
        return Response(
            {"message": f"All employees deleted successfully. Total records deleted: {total_deleted}"},
            status=status.HTTP_204_NO_CONTENT
        )

class EmployeeFilterView(APIView):
    def get(self, request):
        filters = {}
        first_name = request.GET.get('first_name', None)
        last_name = request.GET.get('last_name', None)
        email = request.GET.get('email', None)
        department = request.GET.get('department', None)

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
from .views import (
    EmployeeListCreateView,
    EmployeeDetailView,
    DeleteAllEmployeesView,
    EmployeeFilterView,
)

urlpatterns = [
    path('employees/', EmployeeListCreateView.as_view(), name='employee_list_create'),  # List and Create
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee_detail'),  # Retrieve, Update, Delete
    path('employees/delete_all/', DeleteAllEmployeesView.as_view(), name='delete_all_employees'),  # Delete All
    path('employees/filter/', EmployeeFilterView.as_view(), name='filter_employees'),  # Filter
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('master.urls')),  # Include the master app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# TODO Test api in postman
# ? 1. Create a New Employee with Files (POST)
# URL: http://127.0.0.1:8000/api/employees/
# Method: POST
# Headers: Content-Type: multipart/form-data
# Body: Form-data (key-value pairs)

# Key	            Value	                Type
# ---------------------------------------------
# first_name	    John	                Text
# last_name	        Doe	                    Text
# email	            john.doe@example.com	Text
# department	    IT	                    Text
# photo	            Select an image file	File
# certificate	    Select a PDF file	    File

# Expected Response:
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "department": "IT",
    "photo": "http://127.0.0.1:8000/media/photos/john.jpg",
    "certificate": "http://127.0.0.1:8000/media/certificates/john_cert.pdf"
}

# ? 2. Retrieve All Employees (GET)
# URL: http://127.0.0.1:8000/api/employees/
# Method: GET
# Description: Retrieves a list of all employees.
# Example Response:

[
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "department": "IT",
        "photo": "http://127.0.0.1:8000/media/photos/john.jpg",
        "certificate": "http://127.0.0.1:8000/media/certificates/john_cert.pdf"
    }
]


# ? 3. Update an Employee with Files (PUT)
# URL: http://127.0.0.1:8000/api/employees/1/
# Method: PUT
# Headers: Content-Type: multipart/form-data
# Body: Form-data (key-value pairs)

# Key	        Value	                    Type
# ----------------------------------------------
# first_name	Jane	                    Text
# last_name	    Doe	                        Text
# email	        jane.doe@example.com	    Text
# department	HR	                        Text
# photo	        Select a new image file	    File
# certificate	Select a new PDF file	    File

# Expected Response:
{
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "department": "HR",
    "photo": "http://127.0.0.1:8000/media/photos/jane.jpg",
    "certificate": "http://127.0.0.1:8000/media/certificates/jane_cert.pdf"
}

# ? 4. Delete an Employee (DELETE)
# URL: http://127.0.0.1:8000/api/employees/1/
# Method: DELETE
# Expected Response: Status Code 204 No Content