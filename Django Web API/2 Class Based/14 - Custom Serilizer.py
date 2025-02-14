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

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    # Customizing fields
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'age', 'grade', 'address']
        read_only_fields = ['full_name']  # Custom read-only field

    def get_full_name(self, obj):
        # Custom method to combine first and last name
        return f"{obj.first_name} {obj.last_name}"


# TODO Create view
# master/views.py

from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

class StudentListCreateView(generics.ListCreateAPIView):
    """
    List all students or create a new student.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a student by ID.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import StudentListCreateView, StudentDetailView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student_list_create'),  # List and Create
    path('students/<int:id>/', StudentDetailView.as_view(), name='student_detail'),  # Retrieve, Update, Delete
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
# ? 1. Create a New Student (POST)
# URL: http://127.0.0.1:8000/api/students/
# Method: POST

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "age": 20,
    "grade": "A",
    "address": "123 Main St, City, Country"
}

# Expected Response:

{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "age": 20,
    "grade": "A",
    "address": "123 Main St, City, Country"
}

# ? 2. List All Students (GET)
# URL: http://127.0.0.1:8000/api/students/
# Method: GET
# Description: Retrieves a list of all students.

[
    {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "age": 20,
        "grade": "A",
        "address": "123 Main St, City, Country"
    }
]

# ? 3. Retrieve Student by ID (GET)
# URL: http://127.0.0.1:8000/api/students/1/
# Method: GET
# Description: Retrieves the details of the student with ID 1.

{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "age": 20,
    "grade": "A",
    "address": "123 Main St, City, Country"
}

# ? 4. Update Student by ID (PUT)
URL: http://127.0.0.1:8000/api/students/1/
Method: PUT

{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "age": 21,
    "grade": "B",
    "address": "456 Main St, City, Country"
}

# Expected Response:

{
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "full_name": "Jane Doe",
    "email": "jane.doe@example.com",
    "age": 21,
    "grade": "B",
    "address": "456 Main St, City, Country"
}

# ? 5. Delete Student by ID (DELETE)
# URL: http://127.0.0.1:8000/api/students/1/
# Method: DELETE
# Description: Deletes the student with ID 1.

# Expected Response:

{
    "message": "Student deleted successfully"
}