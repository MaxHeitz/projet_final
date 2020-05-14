"""projet_indiv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from taskmanager import views

# URLs to acces the different pages
urlpatterns = [
    path('admin/', admin.site.urls),  # Django administration
    path('accounts/', include('django.contrib.auth.urls')),  # Generic views : to connect use 'accounts/login'
    path('projects/', views.projects),  # List of projects of the connected user
    path('project/<int:id_project>', views.project),  # Project and details of this project
    path('task/<int:id_task>', views.task),  # Task and details of this task
    path('newtask/', views.newtask),  # A form to add a new task
    path('updatetask/<int:id_task>', views.updatetask),  # A form to update a already existing task
    path('newjournal/<int:id_task>', views.newjournal),  # A form to add a Journal entry to a task
    path('mytasks/', views.mytasks),  # Lis of the tasks of connected user
    path('donetasks/', views.donetasks),  # List of done tasks
    path('activity/<int:id_project>', views.activity),  # A form to update a already existing task
    path('export/', views.export),  # Exports the data from the app
    path('removetask/<int:id_task>',views.removetask),
    path('newproject/',views.newproject),
    path('search/', views.search),  # Lis of the tasks of connected user


]
