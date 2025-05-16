from rest_framework import serializers
from django.db import transaction
from .models import *

class BulkCreateSerializer(serializers.ListSerializer):
        
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('many', True)
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        model = self.child.Meta.model
        with transaction.atomic():
            instances = [model(**item) for item in validated_data]
            return model.objects.bulk_create(instances)

class ComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = '__all__'

class ComponentCategoryBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ManufacturerBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class BaseComponentSerializer:
    def get_related_object(self, model, field, value):
        try:
            return model.objects.get(**{f"{field}__iexact": value})
        except model.DoesNotExist:
            raise serializers.ValidationError(
                {f"{field}_name": f"Объект '{value}' не найден"}
            )

class ComponentSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    manufacturer_name = serializers.CharField(write_only=True, required=True)
    category_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Component
        fields = [
            'id', 'category', 'category_name', 
            'manufacturer', 'manufacturer_name',
            'model', 'price', 'release_date', 'warranty_months', 'country_of_origin', 'link_to_store'
        ]
        read_only_fields = ['id', 'category', 'manufacturer']

    def validate(self, data):
        manufacturer_name = data.get('manufacturer_name')
        category_name = data.get('category_name')

        try:
            manufacturer = Manufacturer.objects.get(name__iexact=manufacturer_name.strip())
            data['manufacturer_id'] = manufacturer.id
        except Manufacturer.DoesNotExist:
            raise serializers.ValidationError({
                'manufacturer_name': f'Производитель "{manufacturer_name}" не найден'
            })

        try:
            category = ComponentCategory.objects.get(name__iexact=category_name.strip())
            data['category_id'] = category.id
        except ComponentCategory.DoesNotExist:
            raise serializers.ValidationError({
                'category_name': f'Категория "{category_name}" не найдена'
            })

        return data

    def create(self, validated_data):
        validated_data.pop('manufacturer_name', None)
        validated_data.pop('category_name', None)
        return super().create(validated_data)

class BaseComponentDetailSerializer(serializers.ModelSerializer, BaseComponentSerializer):
    component = ComponentSerializer()
    
    class Meta:
        abstract = True
    
    def create(self, validated_data):
        with transaction.atomic():
            component_data = validated_data.pop('component')
            component_serializer = ComponentSerializer(data=component_data)
            component_serializer.is_valid(raise_exception=True)
            component = component_serializer.save()
            return self.Meta.model.objects.create(component=component, **validated_data)
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            component_data = validated_data.pop('component', None)
            
            if component_data:
                component_serializer = ComponentSerializer(
                    instance.component, 
                    data=component_data, 
                    partial=True
                )
                component_serializer.is_valid(raise_exception=True)
                component_serializer.save()
            
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            return instance

class CPUSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = CPU
        fields = '__all__'

class CPUBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = CPU
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class GPUSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = GPU
        fields = '__all__'

class GPUBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = GPU
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class RAMSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = RAM
        fields = '__all__'

class RAMBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = RAM
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class MotherboardSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = Motherboard
        fields = '__all__'

class MotherboardBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = Motherboard
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class SSDSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = SSD
        fields = '__all__'

class SSDBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = SSD
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class HDDSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = HDD
        fields = '__all__'

class HDDBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = HDD
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class PSUSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = PSU
        fields = '__all__'

class PSUBulkSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = PSU
        fields = '__all__'
        list_serializer_class = BulkCreateSerializer

class IncompatibleComponentsSerializer(serializers.ModelSerializer):
    first_component_detail = ComponentSerializer(source='first_component', read_only=True)
    second_component_detail = ComponentSerializer(source='second_component', read_only=True)
    
    class Meta:
        model = IncompatibleComponents
        fields = ['id', 'first_component', 'second_component', 
                 'first_component_detail', 'second_component_detail']
        extra_kwargs = {
            'first_component': {'write_only': True},
            'second_component': {'write_only': True}
        }

class PCCaseSerializer(BaseComponentDetailSerializer):
    class Meta(BaseComponentDetailSerializer.Meta):
        model = PCCase
        fields = '__all__'
