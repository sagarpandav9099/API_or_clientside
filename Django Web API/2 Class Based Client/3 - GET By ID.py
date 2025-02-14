
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
    def get_employee_by_id(employee_id):
        url = f"{EmployeeService.BASE_URL}{employee_id}/"
        response = requests.get(url)
        return response

    @staticmethod
    def get_all_employees():
        url = EmployeeService.BASE_URL
        response = requests.get(url)
        return response
    

# TODO Create Form
# master/forms.py
# No need to create form

# TODO Create view
# master/views.py

from django.views.generic import TemplateView, ListView, DetailView
from .services import EmployeeService

class EmployeeListView(ListView):
    template_name = 'master/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        response = EmployeeService.get_all_employees()
        return response.json() if response.status_code == 200 else []

class EmployeeDetailView(DetailView):
    template_name = 'master/employee_detail.html'
    context_object_name = 'employee'

    def get_object(self):
        employee_id = self.kwargs['employee_id']
        response = EmployeeService.get_employee_by_id(employee_id)
        return response.json() if response.status_code == 200 else None



# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='list_employees_view'),
    path('employee/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee_detail_view'),
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
    <ul>
        {% for employee in employees %}
            <li><a href="{% url 'employee_detail_view' employee.id %}">{{ employee.first_name }} {{ employee.last_name }}</a></li>
        {% empty %}
            <li>No employees found.</li>
        {% endfor %}
    </ul>
</body>
</html>

# master/templates/master/employee_detail.html

<!DOCTYPE html>
<html>
<head>
    <title>Employee Detail</title>
</head>
<body>
    <h1>Employee Detail</h1>
    {% if employee %}
        <p>First Name: {{ employee.first_name }}</p>
        <p>Last Name: {{ employee.last_name }}</p>
        <p>Email: {{ employee.email }}</p>
        <p>Department: {{ employee.department }}</p>
    {% else %}
        <p>Employee not found.</p>
    {% endif %}
    <a href="{% url 'list_employees_view' %}">Back to Employee List</a>
</body>
</html>



# TODO Run project with different post than api port
python manage.py runserver 9000