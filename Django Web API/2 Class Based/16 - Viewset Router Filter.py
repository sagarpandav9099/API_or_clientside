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
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing course instances.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description', 'instructor', 'duration', 'level']


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
# ? 1. Filter by Title
# URL: http://127.0.0.1:8000/api/courses/?title=Python
# Method: GET
# Description: Retrieves all courses with titles containing "Python".

# ? 2. Filter by Instructor
# URL: http://127.0.0.1:8000/api/courses/?instructor=John+Doe
# Method: GET
# Description: Retrieves all courses taught by "John Doe".

# ? 3. Filter by Level
# URL: http://127.0.0.1:8000/api/courses/?level=Beginner
# Method: GET
# Description: Retrieves all courses at the "Beginner" level.

# ? 4. Filter by Duration
# URL: http://127.0.0.1:8000/api/courses/?duration=40
# Method: GET
# Description: Retrieves all courses with a duration of 40 hours.

# ? 5. Filter by Multiple Criteria
# URL: http://127.0.0.1:8000/api/courses/?title=Python&level=Beginner
# Method: GET
# Description: Retrieves all beginner-level courses with titles containing "Python".