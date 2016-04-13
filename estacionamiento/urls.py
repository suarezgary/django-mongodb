"""estacionamiento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from estacionamiento.views import insert_ticket,create_cashier,delete_cashier,verif_password, add_operation,get_operaciones_fecha,add_estaciona

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^insert_ticket/', insert_ticket ),
    url(r'^create_cashier/', create_cashier ),
    url(r'^delete_cashier/', delete_cashier ),
    url(r'^verif_password/', verif_password ),
    url(r'^add_operation/', add_operation ),
    url(r'^get_ope_fecha/', get_operaciones_fecha ),
    url(r'^add_estaciona/', add_estaciona ),
]
