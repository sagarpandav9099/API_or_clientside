
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
pip install requests
python manage.py runserver


# TODO Install Apps in setting.py

'master',


# TODO Create Service
# master/services.py

import requests

class EmployeeService:
    BASE_URL = 'http://127.0.0.1:8000/api/employees/'

    @staticmethod
    def delete_all_employees():
        response = requests.delete(EmployeeService.BASE_URL)
        return response
    

# TODO Create Form
# master/forms.py

# no need


# TODO Create view
# master/views.py

from django.shortcuts import render
from .services import EmployeeService

def delete_employees_view(request):
    response = EmployeeService.delete_all_employees()
    if response.status_code == 204:
        message = response.json().get('message', 'All employees deleted successfully.')
    else:
        message = 'Failed to delete employees.'
    return render(request, 'master/delete_result.html', {'message': message})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import delete_employees_view

urlpatterns = [
    path('delete/', delete_employees_view, name='delete_employees_view'),
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),
]


# TODO Create Template
# master/templates/master/delete_result.html

<!DOCTYPE html>
<html>
<head>
    <title>Delete Employees</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <a href="{% url 'delete_employees_view' %}">Delete All Employees Again</a>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000


# TODO Testing the Client-Side Implementation
URL: http://127.0.0.1:9000/master/delete/