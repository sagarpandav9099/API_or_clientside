
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
    def get_all_employees():
        return requests.get(EmployeeService.BASE_URL)

    @staticmethod
    def get_employee(employee_id):
        return requests.get(f"{EmployeeService.BASE_URL}{employee_id}/")

    @staticmethod
    def create_employee(employee_data):
        return requests.post(EmployeeService.BASE_URL, json=employee_data)

    @staticmethod
    def update_employee(employee_id, employee_data):
        return requests.put(f"{EmployeeService.BASE_URL}{employee_id}/", json=employee_data)

    @staticmethod
    def delete_employee(employee_id):
        return requests.delete(f"{EmployeeService.BASE_URL}{employee_id}/")

    @staticmethod
    def delete_all_employees():
        return requests.delete(f"{EmployeeService.BASE_URL}delete_all/")

    @staticmethod
    def filter_employees(params):
        return requests.get(f"{EmployeeService.BASE_URL}filter/", params=params)
  

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

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .services import EmployeeService

class EmployeeListView(ListView):
    template_name = 'master/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        response = EmployeeService.get_all_employees()
        return response.json() if response.status_code == 200 else []

class EmployeeCreateView(CreateView):
    template_name = 'master/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('list_employees_view')

    def form_valid(self, form):
        response = EmployeeService.create_employee(form.cleaned_data)
        if response.status_code == 201:
            return redirect(self.success_url)
        return super().form_invalid(form)

class EmployeeUpdateView(UpdateView):
    template_name = 'master/employee_form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('list_employees_view')

    def get_initial(self):
        response = EmployeeService.get_employee(self.kwargs['employee_id'])
        if response.status_code == 200:
            return response.json()
        return super().get_initial()

    def form_valid(self, form):
        response = EmployeeService.update_employee(self.kwargs['employee_id'], form.cleaned_data)
        if response.status_code == 200:
            return redirect(self.success_url)
        return super().form_invalid(form)

class EmployeeDeleteView(DeleteView):
    success_url = reverse_lazy('list_employees_view')

    def get(self, request, *args, **kwargs):
        EmployeeService.delete_employee(self.kwargs['employee_id'])
        return redirect(self.success_url)

class EmployeeDeleteAllView(View):
    success_url = reverse_lazy('list_employees_view')
    template_name = 'master/employee_confirm_delete_all.html'

    def post(self, request, *args, **kwargs):
        EmployeeService.delete_all_employees()
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class EmployeeFilterView(FormView):
    template_name = 'master/employee_list.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('filter_employees_view')

    def form_valid(self, form):
        params = form.cleaned_data
        response = EmployeeService.filter_employees(params)
        employees = response.json() if response.status_code == 200 else []
        return render(self.request, self.template_name, {'form': form, 'employees': employees})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import (
    EmployeeListView, EmployeeCreateView, EmployeeUpdateView,
    EmployeeDeleteView, EmployeeDeleteAllView, EmployeeFilterView
)

urlpatterns = [
    path('list/', EmployeeListView.as_view(), name='list_employees_view'),
    path('create/', EmployeeCreateView.as_view(), name='create_employee_view'),
    path('update/<int:employee_id>/', EmployeeUpdateView.as_view(), name='update_employee_view'),
    path('delete/<int:employee_id>/', EmployeeDeleteView.as_view(), name='delete_employee_view'),
    path('delete_all/', EmployeeDeleteAllView.as_view(), name='delete_all_employees_view'),
    path('filter/', EmployeeFilterView.as_view(), name='filter_employees_view'),
]


# TODO add urls into project's urls.py
# ECommerce/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),  # Client-side app URLs
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
    <ul>
        {% for employee in employees %}
            <li>{{ employee.first_name }} {{ employee.last_name }} - {{ employee.email }} - {{ employee.department }}
                <a href="{% url 'update_employee_view' employee.id %}">Edit</a>
                <a href="{% url 'delete_employee_view' employee.id %}">Delete</a>
            </li>
        {% empty %}
            <li>No employees found.</li>
        {% endfor %}
    </ul>
    <a href="{% url 'create_employee_view' %}">Create New Employee</a>
    <a href="{% url 'delete_all_employees_view' %}">Delete All Employees</a>

    <h2>Filter Employees</h2>
    <form method="get" action="{% url 'filter_employees_view' %}">
        First Name: <input type="text" name="first_name">
        Last Name: <input type="text" name="last_name">
        Email: <input type="email" name="email">
        Department: <input type="text" name="department">
        <button type="submit">Filter</button>
    </form>
</body>
</html>


# master/templates/master/employee_form.html

<!DOCTYPE html>
<html>
<head>
    <title>Create/Update Employee</title>
</head>
<body>
    <h1>{% if form.instance.id %}Update{% else %}Create{% endif %} Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">{% if form.instance.id %}Update{% else %}Create{% endif %}</button>
    </form>
    <a href="{% url 'list_employees_view' %}">Back to List</a>
</body>
</html>



# master/templates/master/employee_confirm_delete_all.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete All Employees</title>
</head>
<body>
    <h1>Are you sure you want to delete all employees?</h1>
    <form method="post" action="{% url 'delete_all_employees_view' %}">
        {% csrf_token %}
        <button type="submit">Yes, Delete All</button>
    </form>
    <br>
    <a href="{% url 'list_employees_view' %}">Cancel</a>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000


# TODO Testing the Client-Side Implementation
# List Employees 
URL: http://127.0.0.1:9000/master/list/

# Create Employee 
URL: http://127.0.0.1:9000/master/create/