
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
    def get_all_employees(filters=None):
        response = requests.get(EmployeeService.BASE_URL, params=filters)
        return response
    

# TODO Create Form
# master/forms.py

from django import forms

class EmployeeFilterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    department = forms.CharField(max_length=100, required=False)


# TODO Create view
# master/views.py

from django.shortcuts import render
from .forms import EmployeeFilterForm
from .services import EmployeeService

def list_employees_view(request):
    form = EmployeeFilterForm(request.GET or None)
    employees = []
    if form.is_valid():
        response = EmployeeService.get_all_employees(filters=form.cleaned_data)
        employees = response.json() if response.status_code == 200 else []
    return render(request, 'master/employee_list.html', {'form': form, 'employees': employees})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import list_employees_view

urlpatterns = [    
    path('list/', list_employees_view, name='list_employees_view'),
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
# master/templates/master/employee_list.html

<!DOCTYPE html>
<html>
<head>
    <title>Employee List</title>
</head>
<body>
    <h1>Employee List</h1>
    <form method="get">
        {{ form.as_p }}
        <button type="submit">Filter Employees</button>
    </form>
    <ul>
        {% for employee in employees %}
            <li>{{ employee.first_name }} {{ employee.last_name }} - {{ employee.email }} - {{ employee.department }}</li>
        {% empty %}
            <li>No employees found.</li>
        {% endfor %}
    </ul>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000


# TODO Testing the Client-Side Implementation
URL: http://127.0.0.1:9000/master/list/