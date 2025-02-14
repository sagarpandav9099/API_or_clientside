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

from rest_framework import generics
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
    List all suppliers.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


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
# ? 1. Create a New Supplier (POST)
# URL: http://127.0.0.1:8000/api/suppliers/create/
# Method: POST

{
    "name": "John Doe",
    "contact_email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, Anytown, USA",
    "company_name": "Doe Industries"
}

# Expected Response:

{
    "id": 1,
    "name": "John Doe",
    "contact_email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, Anytown, USA",
    "company_name": "Doe Industries"
}

# ? 2. List All Suppliers (GET)
# URL: http://127.0.0.1:8000/api/suppliers/
# Method: GET
# Description: Retrieves a list of all suppliers.
# Example Response:

[
    {
        "id": 1,
        "name": "John Doe",
        "contact_email": "john.doe@example.com",
        "phone_number": "+1234567890",
        "address": "123 Main St, Anytown, USA",
        "company_name": "Doe Industries"
    }
]

# ? 3. Retrieve Supplier by ID (GET)
# URL: http://127.0.0.1:8000/api/suppliers/1/
# Method: GET
# Description: Retrieves the details of the supplier with ID 1.
# Example Response:

{
    "id": 1,
    "name": "John Doe",
    "contact_email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, Anytown, USA",
    "company_name": "Doe Industries"
}

# ? 4. Update Supplier by ID (PUT)
# URL: http://127.0.0.1:8000/api/suppliers/1/update/
# Method: PUT

{
    "name": "Johnathan Doe",
    "contact_email": "johnathan.doe@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, Anytown, USA",
    "company_name": "Doe Industries"
}

# Expected Response:

{
    "id": 1,
    "name": "Johnathan Doe",
    "contact_email": "johnathan.doe@example.com",
    "phone_number": "+1234567890",
    "address": "123 Main St, Anytown, USA",
    "company_name": "Doe Industries"
}

# ? 5. Delete Supplier by ID (DELETE)
# URL: http://127.0.0.1:8000/api/suppliers/1/delete/
# Method: DELETE
# Description: Deletes the supplier with ID 1.
# Expected Response:

{
    "message": "Supplier deleted successfully."
}