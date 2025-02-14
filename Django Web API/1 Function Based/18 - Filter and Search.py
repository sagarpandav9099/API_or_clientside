# Difference Between Filtering and Searching

# Filtering:
# - It is about restricting the queryset based on specific criteria. You specify fields and exact matches or conditions to filter the data. For example, you might filter teachers by their subject or city.
# - It is generally more precise and is used when you want to retrieve data that matches specific attributes or conditions.

# Searching:
# - It allows for a more flexible query, usually involving textual data. It performs a broader search across multiple fields and often uses a contains or icontains query to find matches within the text.
# - It is more flexible and is typically used for user-driven searches where exact criteria aren't known or specified.

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
from rest_framework import filters
from rest_framework import status
from .models import Teacher
from .serializers import TeacherSerializer

@api_view(['GET'])
def teacher_list(request):
    """
    List all teachers with filtering and searching.
    """
    # Setup filter and search backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'city']
    search_fields = ['first_name', 'last_name', 'subject', 'city']

    # Retrieve query parameters
    filter_params = {field: request.GET.get(field) for field in filterset_fields if request.GET.get(field)}
    search_query = request.GET.get('search', '')

    # Filter and search the queryset
    queryset = Teacher.objects.all()

    # Apply filtering
    if filter_params:
        queryset = queryset.filter(**filter_params)

    # Apply searching
    if search_query:
        queryset = queryset.filter(
            first_name__icontains=search_query
        ) | queryset.filter(
            last_name__icontains=search_query
        ) | queryset.filter(
            subject__icontains=search_query
        ) | queryset.filter(
            city__icontains=search_query
        )

    # Serialize data
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
# ? 1. List All Teachers (GET)
# URL: http://127.0.0.1:8000/api/teachers/
# Method: GET
# Description: Retrieves a list of all teachers.

# ? 2. Filter Teachers by Subject
# URL: http://127.0.0.1:8000/api/teachers/?subject=Mathematics
# Method: GET
# Description: Retrieves all teachers teaching Mathematics.

# ? 3. Filter Teachers by City
# URL: http://127.0.0.1:8000/api/teachers/?city=Los Angeles
# Method: GET
# Description: Retrieves all teachers located in Los Angeles.

# ? 4. Search Teachers by Name
# URL: http://127.0.0.1:8000/api/teachers/?search=Alice
# Method: GET
# Description: Searches for teachers with the first name "Alice".

# ? 5. Search Teachers by City
# URL: http://127.0.0.1:8000/api/teachers/?search=York
# Method: GET
# Description: Searches for teachers located in a city containing "York".