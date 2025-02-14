
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
    def get_all_employees():
        response = requests.get(EmployeeService.BASE_URL)
        return response.json() if response.status_code == 200 else []
    

# TODO Create Form
# master/forms.py

# Not required


# TODO Create view
# master/views.py

from django.shortcuts import render
from django.views import View
from .services import EmployeeService

class EmployeeListView(View):
    def get(self, request):
        employees = EmployeeService.get_all_employees()
        return render(request, 'employee_list.html', {'employees': employees})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import EmployeeListView

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
]


# TODO add urls into project's urls.py
# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('master.urls')),
]


# TODO Create Template
# master/templates/master/employee_list.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Employee List</title>
</head>
<body>
    <h1>Employee List</h1>
    <ul>
        {% for employee in employees %}
        <li>{{ employee.first_name }} {{ employee.last_name }} - {{ employee.department }} - {{ employee.email }}</li>
        {% endfor %}
    </ul>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000