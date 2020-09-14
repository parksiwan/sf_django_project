"""sf_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin, auth
from django.urls import path, include
import inventory.views

urlpatterns = [
    path('', inventory.views.home_normal, name='home_normal'),
    path('home_simple/', inventory.views.home_simple, name='home_simple'),
    path('daily_stock/', inventory.views.daily_stock, name='daily_stock'),
    path('tf_stock/', inventory.views.tf_stock, name='tf_stock'),
    path('stock_normal/', inventory.views.stock_normal, name='stock_normal'),
    path('stock_simple/', inventory.views.stock_simple, name='stock_simple'),
    path('home_current_usage/', inventory.views.home_current_usage, name='home_current_usage'),
    path('current_usage/', inventory.views.current_usage, name='current_usage'),
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls', namespace="todo")),
    #path('account/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

admin.site.site_header = "SUSHI FACTORY SCM Data Admin"
admin.site.site_title = "SUSHI FACTORY SCM Data Admin"
admin.site.index_title = "Welcome to SUSHI FACTORY SCM Data Admin"