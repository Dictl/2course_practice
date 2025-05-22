from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class BuildListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        budget = request.GET.get('budget')
        purpose = request.GET.get('purpose')
        priority = request.GET.get('priority')

        print('purpose:', purpose)
        print('priority:', priority)

        # Валидация входных данных
        if not budget or not purpose or not priority:
            return Response({'error': 'Все параметры обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        PURPOSE_MODEL_MAP = {
            'gaming': GamingPc,
            'office': OfficePc,
            'home': MultimediaPc,
            'workstation': Workstation,
        }

        purpose = request.GET.get('purpose')
        model = PURPOSE_MODEL_MAP.get(purpose.lower())
        if not model:
            return Response({'error': 'Некорректное значение purpose'}, status=400)

        data = model.objects.all()

        PRIORITY_FIELD_MAP = {
            'balanced': 'balanced_coefficient',
            'cpu': 'cpu_priority_coefficient',
            'gpu': 'gpu_priority_coefficient',
            'storage': 'ram_memory_priority_coefficient',
        }

        priority_field = PRIORITY_FIELD_MAP.get(priority.lower())
        if not priority_field:
            return Response({'error': 'Некорректное значение priority'}, status=400)

        total = model.objects.aggregate(sum=Sum(priority_field))['sum'] or 0
        print(f'Сумма по полю {priority_field} для {purpose}:', total)

        # budget и total должны быть числами
        part_budget = float(budget) / float(total) if total else 0
        print(f'Часть бюджета на 1 коэффициент: {part_budget}')

        component_budgets = []
        for obj in data:
            coef = float(getattr(obj, priority_field, 0) or 0)
            component_budget = float(part_budget) * coef
            print(f'Компонент: {str(obj)}, бюджет: {component_budget}')
            component_budgets.append({
                'id': obj.pk,
                'name': str(obj),
                'coefficient': coef,
                'component_budget': component_budget,
            })

        import itertools

        category_ids = [
            (1, "Процессоры"),
            (2, "Видеокарты"),
            (3, "Материнские платы"),
            (4, "Оперативная память"),
            (5, "Накопители SSD"),
            # (6, "Жесткие диски"),  # Исключено
            (7, "Блоки питания"),
            (8, "Корпуса"),
            (9, "Системы охлаждения"),
        ]

        components_by_category = []
        for cat_id, cat_name in category_ids:
            info = next((c for c in component_budgets if c['id'] == cat_id), None)
            if not info:
                return Response({'error': f'Нет бюджета для категории {cat_name}'}, status=400)
            comps = list(Component.objects.filter(category_id=cat_id, price__lte=info['component_budget']))
            if not comps:
                return Response({'error': f'Нет подходящих компонентов для категории {cat_name}'}, status=400)
            components_by_category.append(comps)

        builds = []
        for idx, combination in enumerate(itertools.islice(itertools.product(*components_by_category), 20), 1):
            total_price = sum(comp.price for comp in combination)
            builds.append({
                'id': idx,
                'name': f'Сборка #{idx}',
                'totalPrice': total_price,
                'components': [
                    {'name': str(comp), 'price': comp.price, 'category': cat_name}
                    for comp, (_, cat_name) in zip(combination, category_ids)
                ]
            })

        return Response(builds, status=status.HTTP_200_OK)

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