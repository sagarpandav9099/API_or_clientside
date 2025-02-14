
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
    def update_employee(employee_id, employee_data):
        response = requests.put(f"{EmployeeService.BASE_URL}{employee_id}/", json=employee_data)
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

from django.views import View
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .services import EmployeeService

class UpdateEmployeeView(View):
    template_name = 'master/update_employee.html'

    def get(self, request, employee_id):
        form = EmployeeForm()
        return render(request, self.template_name, {'form': form, 'employee_id': employee_id})

    def post(self, request, employee_id):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            response = EmployeeService.update_employee(employee_id, form.cleaned_data)
            if response.status_code == 200:
                return redirect('employee_list_view')  # Redirect after successful update
            else:
                form.add_error(None, response.json())
        return render(request, self.template_name, {'form': form, 'employee_id': employee_id})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import UpdateEmployeeView

urlpatterns = [
    path('employees/update/<int:employee_id>/', UpdateEmployeeView.as_view(), name='update_employee_view'),
]


# TODO add urls into project's urls.py
# ECommerce/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),
]


# TODO Create Template
# master/templates/master/update_employee.html

<!DOCTYPE html>
<html>
<head>
    <title>Update Employee</title>
</head>
<body>
    <h1>Update Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Update Employee</button>
    </form>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000