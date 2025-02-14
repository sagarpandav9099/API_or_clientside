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


# TODO Install Package for filter

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

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


# TODO Create view
# master/views.py

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Supplier
from .serializers import SupplierSerializer

class SupplierCreateView(generics.CreateAPIView):
    """
    Create a new supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierListView(generics.ListAPIView):
    """
    List all suppliers with filtering, searching, and ordering.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'contact_email', 'company_name']
    search_fields = ['name', 'contact_email', 'company_name', 'address']
    ordering_fields = ['name', 'company_name']
    ordering = ['name']  # Default ordering


class SupplierDetailView(generics.RetrieveAPIView):
    """
    Retrieve a supplier by ID.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierUpdateView(generics.UpdateAPIView):
    """
    Update a supplier by ID.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierDeleteView(generics.DestroyAPIView):
    """
    Delete a supplier by ID.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import (
    SupplierCreateView,
    SupplierListView,
    SupplierDetailView,
    SupplierUpdateView,
    SupplierDeleteView
)

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('suppliers/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
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
# ? 1. Filter Suppliers by Name
# URL: http://127.0.0.1:8000/api/suppliers/?name=John
# Method: GET
# Description: Retrieves all suppliers with the name "John".

# ? 2. Search Suppliers by Address
# URL: http://127.0.0.1:8000/api/suppliers/?search=Main St
# Method: GET
# Description: Searches for suppliers whose address contains "Main St".

# ? 3. Order Suppliers by Company Name
# URL: http://127.0.0.1:8000/api/suppliers/?ordering=company_name
# Method: GET
# Description: Retrieves all suppliers ordered by company name.

# ? 4. Filter by Multiple Criteria
# URL: http://127.0.0.1:8000/api/suppliers/?name=John&company_name=Doe Industries
# Method: GET
# Description: Retrieves all suppliers with the name "John" and company name "Doe Industries".