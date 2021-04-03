"""bot_cs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from main import views
from django.urls import path,include
from django.contrib.auth import views as ViewsClass
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'bots', views.BotsViewSet)
router.register(r'botsshow', views.BotsShowViewSet)


urlpatterns = [
    path('', views.main,name='main'),
    path('logs/',views.logs,name='logs'),
    path('logs/<str:login>',views.logs_for,name='logs_for'),
    path('items/',views.items,name='items'),
    path('items/<str:login>',views.items_for,name='items_for'),
    path('setting/',views.settings,name='setting'),
    path('setting/save/',views.settingsave,name='settingsave'),
    path('login/', ViewsClass.LoginView.as_view(template_name ='main/login.html'), name='login'),
    path('logout/',views.logouto, name='logout'),
    path('save/',views.save,name='save'),
    path('boton/<str:login>',views.bot_on,name='boton'),
    path('botoff/<str:login>',views.bot_off,name='botoff'),
    path('api/', include(router.urls)),
]


# login : admin
# pass: Admin1234
