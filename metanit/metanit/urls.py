"""
URL configuration for metanit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls import include
from hello import views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', ComponentCategoryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'cpus', CPUViewSet)
router.register(r'gpus', GPUViewSet)
router.register(r'rams', RAMViewSet)
router.register(r'motherboards', MotherboardViewSet)
router.register(r'ssds', SSDViewSet)
router.register(r'hdds', HDDViewSet)
router.register(r'psus', PSUViewSet)
router.register(r'incompatible', IncompatibleComponentsViewSet)
router.register(r'cases', PCCaseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello.urls')),  # Подключаем URL вашего приложения
    path('api/', include(router.urls)),
    path("admin/", admin.site.urls)
]
