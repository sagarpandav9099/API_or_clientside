
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
    def create_employee(data):
        response = requests.post(EmployeeService.BASE_URL, data=data)
        return response


# TODO Create Form
# master/forms.py

from django import forms

class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    department = forms.CharField(max_length=100)


# TODO Create view
# master/views.py

from django.shortcuts import render
from django.views import View
from .forms import EmployeeForm
from .services import EmployeeService

class EmployeeCreateView(View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'employee_form.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            response = EmployeeService.create_employee(form.cleaned_data)
            if response.status_code == 201:
                return render(request, 'employee_success.html')
            else:
                return render(request, 'employee_form.html', {'form': form, 'errors': response.json()})
        return render(request, 'employee_form.html', {'form': form})


# TODO add urls into app's urls.py
# master/urls.py

from django.urls import path
from .views import EmployeeCreateView

urlpatterns = [
    path('employee/create/', EmployeeCreateView.as_view(), name='create_employee'),
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
# master/templates/master/employee_form.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Create Employee</title>
</head>
<body>
    <h1>Create Employee</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
    {% if errors %}
    <div style="color:red;">
        <p>Error submitting the form:</p>
        <ul>
            {% for key, value in errors.items %}
                <li>{{ key }}: {{ value }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</body>
</html>


# master/templates/master/success.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Success</title>
</head>
<body>
    <h1>Employee Created Successfully!</h1>
    <a href="{% url 'create_employee' %}">Create another employee</a>
</body>
</html>


# TODO Run project with different post than api port
python manage.py runserver 9000