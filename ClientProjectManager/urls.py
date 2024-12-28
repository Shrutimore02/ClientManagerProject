"""
URL configuration for ClientProjectManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from clients.views import (ClientListCreateAPIView,
    ClientRetrieveUpdateDestroyAPIView,
    ClientDetailAPIView,
    ProjectListForUserAPIView,
    create_project_for_client)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', create_project_for_client, name='create-project-for-client'),
    path('projects/', ProjectListForUserAPIView.as_view(), name='project-list-for-user'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),

]
