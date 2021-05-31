"""softcar URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from sc.views import vista1
from sc.views import registrartrabajo
from sc.views import registrarrepuesto
from sc.views import modificarrepuesto
from sc.views import modificarestado
from sc.views import registrarcliente
from sc.views import registrarcliente2
from sc.views import modificarestado2
from sc.views import modificarestado3
from sc.views import crearepuesto
from sc.views import crearepuesto2
from sc.views import modificarrespuesto2
from sc.views import registrarvehiculo
from sc.views import registrarvehiculo2
from sc.views import registrartrabajo2
from sc.views import logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='index.html')),
    path('accounts/profile/', vista1 , name='vista1'),
    path('vista1',vista1, name='vista1'),
    path('registrartrabajo',registrartrabajo, name='registrartrabajo'),
    path('registrarrepuesto',registrarrepuesto, name='registrarrepuesto'),
    path('modificarrepuesto',modificarrepuesto, name='modificarrepuesto'),
    path('modificarestado',modificarestado, name='modificarestado'),
    path('registrarcliente',registrarcliente, name='registrarcliente'),
    path('registrarcliente2',registrarcliente2, name='registrarcliente2'),
    path('modificarestado2',modificarestado2, name='modificarestado2'),
    path('modificarestado3',modificarestado3, name='modificarestado3'),
    path('crearepuesto',crearepuesto, name='crearepuesto'),
    path('crearepuesto2',crearepuesto2, name='crearepuesto2'),
    path('modificarrespuesto2',modificarrespuesto2, name='modificarrespuesto2'),
    path('registrarvehiculo',registrarvehiculo, name='registrarvehiculo'),
    path('registrarvehiculo2',registrarvehiculo2, name='registrarvehiculo2'),
    path('registrartrabajo2',registrartrabajo2, name='registrartrabajo2'),
    path('accounts/profile/logout_view',logout_view, name='accounts/profile/logout_view'),
]
