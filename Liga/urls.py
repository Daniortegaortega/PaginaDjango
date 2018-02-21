"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from Liga.views import comprarSkin,skins,saldoUser,usernameChange,index,registrarUser,vender,ligas,inscribirseLiga,venderSkin,borrarLiga,mostrarPerfil,contactomail
from django.contrib.auth.views import login, logout


urlpatterns = [
    path('index/',index.as_view(),name='index'),

    path('registro/',registrarUser,name='registro'),
    path('login/', login, {'template_name':'login.html'},name='login'),
    path('logout/',logout,{'template_name':'index.html'}, name='logout'),

    path('saldo/<int:user_id>',saldoUser,name='saldo'),
    path('username/<int:user_id>',usernameChange,name="username"),

    path('perfil/',mostrarPerfil,name="perfil"),
    path('perfil/<int:liga_id><int:user_id>',borrarLiga,name="borrarLiga"),

    path('skins/', skins, name='skins'),
    path('skins/<int:skin_id><int:user_id>', comprarSkin, name="comprarSkin"),

    path('vender/',vender.as_view(),name='vender'),
    path('vender/<int:user_id>',venderSkin,name='venderSkin'),

    path('ligas/',ligas, name="ligas"),
    path('ligas/<int:user_id><int:liga_id>',inscribirseLiga,name="inscribirse"),

    path('contactar/',contactomail.as_view(), name="contactar"),
]
