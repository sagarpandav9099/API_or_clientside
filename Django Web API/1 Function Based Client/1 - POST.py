
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
    def create_employee(employee_data):
        response = requests.post(EmployeeService.BASE_URL, json=employee_data)
        return response


# TODO Create Form
# master/forms.py

from django import forms

class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=100, required=True)

# TODO Create view
# master/views.py

from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .services import EmployeeService

def create_employee_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            response = EmployeeService.create_employee(form.cleaned_data)
            if response.status_code == 201:
                return render(request, 'master/success.html', {'employee': response.json()})
            else:
                form.add_error(None, response.json())
    else:
        form = EmployeeForm()
    return render(request, 'master/employee_form.html', {'form': form})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import create_employee_view

urlpatterns = [
    path('create/', create_employee_view, name='create_employee_view'),
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
# master/templates/master/employee_form.html

<!DOCTYPE html>
<html>
<head>
    <title>Create Employee</title>
</head>
<body>
    <h1>Create a New Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Create Employee</button>
    </form>
</body>
</html>

# master/templates/master/success.html

<!DOCTYPE html>
<html>
<head>
    <title>Employee Created</title>
</head>
<body>
    <h1>Employee Created Successfully</h1>
    <p>First Name: {{ employee.first_name }}</p>
    <p>Last Name: {{ employee.last_name }}</p>
    <p>Email: {{ employee.email }}</p>
    <p>Department: {{ employee.department }}</p>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000


# TODO Testing the Client-Side Implementation
URL: http://127.0.0.1:9000/master/create/