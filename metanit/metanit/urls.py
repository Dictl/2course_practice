from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ComponentCategoryViewSet, ManufacturerViewSet, ComponentViewSet,
    CPUViewSet, GPUViewSet, RAMViewSet, MotherboardViewSet, SSDViewSet,
    HDDViewSet, PSUViewSet, IncompatibleComponentsViewSet, PCCaseViewSet,
    BuildListAPIView
)

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
    path('', include('hello.urls')),

    path('api/builds', BuildListAPIView.as_view()),   # без слэша
    path('api/builds/', BuildListAPIView.as_view()),  # со слэшем

    path('api/', include(router.urls)),

]

