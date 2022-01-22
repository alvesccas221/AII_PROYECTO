"""AII URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from principal import views

urlpatterns = [
    path('', views.inicio),
    path('cargar/', views.populateDB),
    path('juegos/', views.listaJuegos),
    path('puntuaciones/', views.listaPuntuaciones),
    path('buscarjuegos/', views.buscarJuego),
    path('buscarrangoprecio/', views.buscarRango),
    path('recomiendajuego/', views.recomiendaJuego),
    path('cargamatriz/', views.loadRS),
    path('recomiendajuegosimilar/', views.similarJuego),
    path('admin/', admin.site.urls),
]
