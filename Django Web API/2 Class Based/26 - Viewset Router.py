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


# TODO Install Package

pip install Pillow


# TODO Install Apps in setting.py

# settings.py

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

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    level = models.CharField(max_length=50)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # Image field
    syllabus = models.FileField(upload_to='course_syllabus/', null=True, blank=True)  # Document field

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('master.urls')),  # Include the master app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# TODO Test api in postman
# ? 1. Create a New Course with Files (POST)
# URL: http://127.0.0.1:8000/api/courses/
# Method: POST
# Headers: Content-Type: multipart/form-data
# Body: Form-data (key-value pairs)

# Key	            Value	                    Type
# ----------------------------------------------------
# title	            Introduction to Python	    Text
# description	    Learn the basics of Python	Text
# instructor	    John Doe	                Text
# duration	        40	                        Text
# level	            Beginner	                Text
# image	            Select an image file	    File
# syllabus	        Select a PDF file	        File

# Expected Response:

{
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn the basics of Python programming.",
    "instructor": "John Doe",
    "duration": 40,
    "level": "Beginner",
    "image": "http://127.0.0.1:8000/media/course_images/python.jpg",
    "syllabus": "http://127.0.0.1:8000/media/course_syllabus/python_syllabus.pdf"
}

# ? 2. Retrieve All Courses (GET)
# URL: http://127.0.0.1:8000/api/courses/
# Method: GET
# Description: Retrieves a list of all courses.

# ? 3. Update a Course with Files (PUT)
# URL: http://127.0.0.1:8000/api/courses/1/
# Method: PUT
# Headers: Content-Type: multipart/form-data
# Body: Form-data (key-value pairs)

# Key	        Value	                        Type
# --------------------------------------------------
# title	        Advanced Python	                Text
# description	Learn advanced Python concepts	Text
# instructor	Jane Doe	                    Text
# duration	    60	                            Text
# level	        Advanced	                    Text
# image	        Select a new image file	        File
# syllabus	    Select a new PDF file	        File

# Expected Response:

{
    "id": 1,
    "title": "Advanced Python",
    "description": "Learn advanced Python programming concepts.",
    "instructor": "Jane Doe",
    "duration": 60,
    "level": "Advanced",
    "image": "http://127.0.0.1:8000/media/course_images/advanced_python.jpg",
    "syllabus": "http://127.0.0.1:8000/media/course_syllabus/advanced_python_syllabus.pdf"
}

# ? 4. Delete a Course (DELETE)
# URL: http://127.0.0.1:8000/api/courses/1/
# Method: DELETE
# Expected Response: Status Code 204 No Content