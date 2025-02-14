
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
    BASE_URL = "http://127.0.0.1:8000/api/employees/"

    @staticmethod
    def get_employees():
        response = requests.get(EmployeeService.BASE_URL)
        return response.json()

    @staticmethod
    def get_employee(employee_id):
        response = requests.get(f"{EmployeeService.BASE_URL}{employee_id}/")
        return response.json()

    @staticmethod
    def create_employee(data):
        response = requests.post(EmployeeService.BASE_URL, json=data)
        return response.json()

    @staticmethod
    def update_employee(employee_id, data):
        response = requests.put(f"{EmployeeService.BASE_URL}{employee_id}/", json=data)
        return response.json()

    @staticmethod
    def delete_employee(employee_id):
        response = requests.delete(f"{EmployeeService.BASE_URL}{employee_id}/")
        return response.status_code
    

# TODO Create Form
# master/forms.py

from django import forms

class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=100, required=True)

    def clean_department(self):
        allowed_departments = ['Engineering', 'HR', 'Sales', 'Marketing']
        department = self.cleaned_data.get('department')
        if department not in allowed_departments:
            raise forms.ValidationError(f"Department must be one of {allowed_departments}.")
        return department


# TODO Create view
# master/views.py

from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .services import EmployeeService

def employee_list(request):
    employees = EmployeeService.get_employees()
    return render(request, 'master/employee_list.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = EmployeeService.get_employee(employee_id)
    return render(request, 'master/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            EmployeeService.create_employee(form.cleaned_data)
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'master/employee_form.html', {'form': form})

def employee_update(request, employee_id):
    employee = EmployeeService.get_employee(employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            EmployeeService.update_employee(employee_id, form.cleaned_data)
            return redirect('employee_list')
    else:
        form = EmployeeForm(initial=employee)
    return render(request, 'master/employee_form.html', {'form': form})

def employee_delete(request, employee_id):
    EmployeeService.delete_employee(employee_id)
    return redirect('employee_list')


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/update/<int:employee_id>/', views.employee_update, name='employee_update'),
    path('employee/delete/<int:employee_id>/', views.employee_delete, name='employee_delete'),
]

# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),  # Client-side app URLs
]


# TODO Create Template
# master/templates/master/employee_list.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee List</title>
</head>
<body>
    <h1>Employee List</h1>
    <ul>
        {% for employee in employees %}
            <li>
                <a href="{% url 'employee_detail' employee.id %}">
                    {{ employee.first_name }} {{ employee.last_name }}
                </a>
            </li>
        {% endfor %}
    </ul>
    <br>
    <a href="{% url 'employee_create' %}">Add New Employee</a>
</body>
</html>


# master/templates/master/employee_detail.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Detail</title>
</head>
<body>
    <h1>{{ employee.first_name }} {{ employee.last_name }}</h1>
    <p><strong>Email:</strong> {{ employee.email }}</p>
    <p><strong>Department:</strong> {{ employee.department }}</p>
    <br>
    <a href="{% url 'employee_update' employee.id %}">Edit Employee</a> |
    <a href="{% url 'employee_confirm_delete' employee.id %}">Delete Employee</a> |
    <a href="{% url 'employee_list' %}">Back to Employee List</a>
</body>
</html>


# master/templates/master/employee_form.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if form.instance.id %}Edit{% else %}Add New{% endif %} Employee</title>
</head>
<body>
    <h1>{% if form.instance.id %}Edit{% else %}Add New{% endif %} Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">{% if form.instance.id %}Update{% else %}Create{% endif %} Employee</button>
    </form>
    <br>
    <a href="{% url 'employee_list' %}">Back to Employee List</a>
</body>
</html>

# master/templates/master/employee_confirm_delete.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Employee</title>
</head>
<body>
    <h1>Delete Employee</h1>
    <p>Are you sure you want to delete {{ employee.first_name }} {{ employee.last_name }}?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
    </form>
    <br>
    <a href="{% url 'employee_detail' employee.id %}">Cancel</a>
</body>
</html>



# TODO Run project with different post than api port
python manage.py runserver 9000