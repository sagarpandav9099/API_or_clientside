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

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.title

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# TODO Create view
# master/views.py

from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

# Create a router and register our viewset with it.
# basename will generate URL patterns with the following names:
    # List: course-list
    # Detail: course-detail
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

# The API URLs are now determined automatically by the router.
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
# ? 1. Create a New Course (POST)
# URL: http://127.0.0.1:8000/api/courses/
# Method: POST

{
    "title": "Introduction to Python",
    "description": "Learn the basics of Python programming.",
    "instructor": "John Doe",
    "duration": 40,
    "level": "Beginner"
}

# Expected Response:

{
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn the basics of Python programming.",
    "instructor": "John Doe",
    "duration": 40,
    "level": "Beginner"
}

# ? 2. List All Courses (GET)
# URL: http://127.0.0.1:8000/api/courses/
# Method: GET
# Description: Retrieves a list of all courses.
# Example Response:

[
    {
        "id": 1,
        "title": "Introduction to Python",
        "description": "Learn the basics of Python programming.",
        "instructor": "John Doe",
        "duration": 40,
        "level": "Beginner"
    }
]

# ? 3. Retrieve Course by ID (GET)
# URL: http://127.0.0.1:8000/api/courses/1/
# Method: GET
# Description: Retrieves the details of the course with ID 1.
# Example Response:

{
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn the basics of Python programming.",
    "instructor": "John Doe",
    "duration": 40,
    "level": "Beginner"
}

# ? 4. Update Course by ID (PUT)
# URL: http://127.0.0.1:8000/api/courses/1/
# Method: PUT

{
    "title": "Advanced Python",
    "description": "Learn advanced Python programming concepts.",
    "instructor": "Jane Doe",
    "duration": 60,
    "level": "Advanced"
}

# Expected Response:

{
    "id": 1,
    "title": "Advanced Python",
    "description": "Learn advanced Python programming concepts.",
    "instructor": "Jane Doe",
    "duration": 60,
    "level": "Advanced"
}

# ? 5. Delete Course by ID (DELETE)
# URL: http://127.0.0.1:8000/api/courses/1/
# Method: DELETE
# Description: Deletes the course with ID 1.
# Expected Response:

{
    "message": "Course deleted successfully."
}