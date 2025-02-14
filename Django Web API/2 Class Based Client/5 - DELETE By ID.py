
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
    def delete_employee(employee_id):
        url = f"{EmployeeService.BASE_URL}{employee_id}/"
        response = requests.delete(url)
        return response


# TODO Create Form
# master/forms.py

from django import forms

class EmployeeForm(forms.Form):
    employee_id = forms.IntegerField(required=True, label="Employee ID")


# TODO Create view
# master/views.py

from django.views import View
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .services import EmployeeService

class DeleteEmployeeView(View):
    template_name = 'master/delete_employee_form.html'
    
    def get(self, request):
        form = EmployeeForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            response = EmployeeService.delete_employee(employee_id)
            if response.status_code == 204:
                return render(request, 'master/success.html', {'message': 'Employee deleted successfully.'})
            else:
                return render(request, 'master/failure.html', {'message': 'Employee not found or could not be deleted.'})
        return render(request, self.template_name, {'form': form})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import DeleteEmployeeView

urlpatterns = [
    path('delete/', DeleteEmployeeView.as_view(), name='delete_employee_view'),
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
# master/templates/master/delete_employee_form.html

<!DOCTYPE html>
<html>
<head>
    <title>Delete Employee</title>
</head>
<body>
    <h1>Delete Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Delete Employee</button>
    </form>
</body>
</html>


# master/templates/master/success.html

<!DOCTYPE html>
<html>
<head>
    <title>Success</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <a href="{% url 'delete_employee_view' %}">Delete Another Employee</a>
</body>
</html>


# master/templates/master/failure.html

<!DOCTYPE html>
<html>
<head>
    <title>Failure</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <a href="{% url 'delete_employee_view' %}">Try Again</a>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000