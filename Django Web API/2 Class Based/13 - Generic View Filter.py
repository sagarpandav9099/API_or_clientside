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

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

 
 # TODO Do migration
python manage.py makemigrations master
python manage.py migrate master
    

# TODO Create serializers.py in apps directory
# master/serializers.py

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # Ensure that fields are not empty
    name = serializers.CharField(required=True, allow_blank=False)
    description = serializers.CharField(required=True, allow_blank=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    stock = serializers.IntegerField(required=True)
    category = serializers.CharField(required=True, allow_blank=False)

    def validate_name(self, value):
        # Custom validation for name
        if value == "":
            raise serializers.ValidationError("Product name must not be empty.")
        return value

    def validate_price(self, value):
        # Ensure price is not negative
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        # Ensure stock is not negative
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


# TODO Create view
# master/views.py

from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    Allows filtering by name, description, price, stock, and category.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned products,
        by filtering against query parameters in the URL.
        """
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)
        price = self.request.query_params.get('price', None)
        stock = self.request.query_params.get('stock', None)
        category = self.request.query_params.get('category', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if description is not None:
            queryset = queryset.filter(description__icontains=description)
        if price is not None:
            queryset = queryset.filter(price=price)
        if stock is not None:
            queryset = queryset.filter(stock=stock)
        if category is not None:
            queryset = queryset.filter(category__icontains=category)

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product by ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),  # List and Create
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),  # Retrieve, Update, Delete
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
# ? 1. Filter by Name
# URL: http://127.0.0.1:8000/api/products/?name=Laptop
# Method: GET
# Description: Retrieves all products with names containing "Laptop".

# ? 2. Filter by Category
# URL: http://127.0.0.1:8000/api/products/?category=Electronics
# Method: GET
# Description: Retrieves all products in the "Electronics" category.

# ? 3. Filter by Price
# URL: http://127.0.0.1:8000/api/products/?price=1500.00
# Method: GET
# Description: Retrieves all products priced at exactly 1500.00.

# ? 4. Filter by Stock
# URL: http://127.0.0.1:8000/api/products/?stock=10
# Method: GET
# Description: Retrieves all products with exactly 10 units in stock.

# ? 5. Filter by Multiple Criteria
# URL: http://127.0.0.1:8000/api/products/?name=Laptop&category=Electronics
# Method: GET
# Description: Retrieves all products with names containing "Laptop" and in the "Electronics" category.