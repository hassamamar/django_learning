"""
URL configuration for my_app project.

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
from django.urls import path, include
from django.views.generic import RedirectView

import Main.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', Main.views.RegisterView.as_view(), name='register'),

    path('', RedirectView.as_view(url='/cars/', permanent=False), name='main'),
    path('cars/', Main.views.CarListView.as_view(), name='cars'),
    path('makers/', Main.views.MakerListView.as_view(), name='makers'),
    path('makers/create', Main.views.MakerCreateView.as_view(), name='create-maker'),
    path('makers/<str:name>/delete/', Main.views.MakerDeleteView.as_view(), name='delete-maker'),
    path('cars/create', Main.views.CarCreateView.as_view(), name='create-car'),
    path('cars/<int:pk>/update/', Main.views.CarUpdateView.as_view(), name='update-car'),
    path('cars/<int:pk>/delete/', Main.views.CarDeleteView.as_view(), name='delete-car'),

]
"""
path('create', None),
    path('delete', None),


    path('makers/delete', None),
    
"""
