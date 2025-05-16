from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Component, ComponentCategory, Manufacturer, CPU, GPU, RAM, Motherboard, SSD, HDD, PSU, IncompatibleComponents, PCCase
from .serializers import *

class ComponentCategoryViewSet(viewsets.ModelViewSet):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = ComponentCategoryBulkSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = ManufacturerBulkSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class ManufacturerBulkViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerBulkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer
    
    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class RAMViewSet(viewsets.ModelViewSet):
    queryset = RAM.objects.all()
    serializer_class = RAMSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class MotherboardViewSet(viewsets.ModelViewSet):
    queryset = Motherboard.objects.all()
    serializer_class = MotherboardSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class SSDViewSet(viewsets.ModelViewSet):
    queryset = SSD.objects.all()
    serializer_class = SSDSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class HDDViewSet(viewsets.ModelViewSet):
    queryset = HDD.objects.all()
    serializer_class = HDDSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class PSUViewSet(viewsets.ModelViewSet):
    queryset = PSU.objects.all()
    serializer_class = PSUSerializer

    def perform_destroy(self, instance):
        with transaction.atomic():
            component = instance.component 
            instance.delete() 
            component.delete() 

class IncompatibleComponentsViewSet(viewsets.ModelViewSet):
    queryset = IncompatibleComponents.objects.all()
    serializer_class = IncompatibleComponentsSerializer

class PCCaseViewSet(viewsets.ModelViewSet):
    queryset = PCCase.objects.all()
    serializer_class = PCCaseSerializer