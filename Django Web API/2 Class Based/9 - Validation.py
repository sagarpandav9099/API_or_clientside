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
    
    # Ensure that fields are not empty
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    department = serializers.CharField(required=True, allow_blank=False)

    def validate_first_name(self, value):
        # Custom validation for first_name
        if not value.isalpha():
            raise serializers.ValidationError("First name should contain only letters.")
        if value == "":
            raise serializers.ValidationError("First name must not be empty.")
        return value

    def validate_last_name(self, value):
        # Custom validation for last_name
        if not value.isalpha():
            raise serializers.ValidationError("Last name should contain only letters.")
        if value == "":
            raise serializers.ValidationError("Last name must not be empty.")
        return value

    def validate_email(self, value):
        # Check if email is not empty
        if value == "":
            raise serializers.ValidationError("Email must not be empty.")
        return value

    def validate_department(self, value):
        # Example of checking allowed departments
        allowed_departments = ['Engineering', 'HR', 'Sales', 'Marketing']
        if value not in allowed_departments:
            raise serializers.ValidationError(f"Department must be one of {allowed_departments}.")
        if value == "":
            raise serializers.ValidationError("Department must not be empty.")
        return value



# TODO Create view
# master/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeList(APIView):
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


class EmployeeDetail(APIView):
    def get_object(self, employee_id):
        try:
            return Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None

    def get(self, request, employee_id):
        employee = self.get_object(employee_id)
        if employee is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, employee_id):
        employee = self.get_object(employee_id)
        if employee is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id):
        employee = self.get_object(employee_id)
        if employee is None:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import EmployeeList, EmployeeDetail

urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='employees_list'),  # Use .as_view() for class-based views
    path('employees/<int:employee_id>/', EmployeeDetail.as_view(), name='employee_detail'),  # Use .as_view() for class-based views
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel access
    path('api/', include('master.urls')),  # Include the URLs from the master app
]



# TODO Test api in postman
# ? 1. Create a New Employee
# Method: POST
# URL: http://127.0.0.1:8000/api/employees/
# - Select Body
# - Choose raw and JSON format.
# - Body

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "department": "Engineering"
}

# Validation Tests:
# Empty Fields Test:

{
    "first_name": "",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "department": "Engineering"
}

# Expected Response:
{
    "first_name": [
        "This field may not be blank.",
        "First name must not be empty."
    ]
}

# Invalid Department Test:
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "department": "Finance"
}

# Expected Response:
{
    "department": [
        "Department must be one of ['Engineering', 'HR', 'Sales', 'Marketing']."
    ]
}