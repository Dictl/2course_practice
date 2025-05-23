from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
import sys

sys.setrecursionlimit(10000)

class BuildListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        budget = request.GET.get('budget')
        purpose = request.GET.get('purpose')
        print(purpose)
        priority = request.GET.get('priority')
        print(priority)

        print('>реквест разобран')

        # Валидация входных данных
        if not budget or not purpose or not priority:
            return Response({'error': 'Все параметры обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        print('>валидация успешна')

        try:
            budget = Decimal(budget)
        except (InvalidOperation, TypeError):
            return Response({'error': 'Бюджет должен быть числом'}, status=400)

        PURPOSE_MODEL_MAP = {
            'gaming': GamingPc,
            'office': OfficePc,
            'home': MultimediaPc,
            'workstation': Workstation,
        }

        model = PURPOSE_MODEL_MAP.get(purpose.lower())
        if not model:
            return Response({'error': 'Некорректное значение purpose'}, status=400)

        PRIORITY_FIELD_MAP = {
            'balanced': 'balanced_coefficient',
            'cpu': 'cpu_priority_coefficient',
            'gpu': 'gpu_priority_coefficient',
            'storage': 'ram_memory_priority_coefficient',
        }

        priority_field = list(model.objects.values_list(PRIORITY_FIELD_MAP.get(priority.lower()), flat = True).order_by('category_id'))
        categories = [float(value) for value in priority_field]
        print(categories)
        cats = [1,2,3,4,5,6,7,8,9]
        sorted_pairs = sorted(zip(categories, cats), key=lambda x: x[0], reverse=True)
        sorted_categories, cats = map(list, zip(*sorted_pairs))
        print(sorted_categories)
        print(cats)

        def generate_builds(max_builds=20):
            print('>начинаю генерить билды')
            builds = []
            # Для каждой категории получаем компоненты, отсортированные по убыванию цены
            category_components = []
            for i in range(len(categories)):
                print('>создаю списки компонентов, текущий i = ', i+1)
                category_components.append(list(Component.objects.filter(
                    category_id=i+1
                ).order_by('-price')))

            # Рекурсивная функция для поиска сборок
            # Рекурсивная функция для поиска сборок
            def backtrack(current_build, remaining_budget, category_index, current_components):
                if len(builds) >= max_builds:
                    return

                if category_index >= len(categories) - 1:
                    # Все категории обработаны - сборка готова
                    total_price = sum(c.price for c in current_build)
                    builds.append({
                        'id': len(builds) + 1,
                        'name': f'Сборка #{len(builds) + 1}',
                        'totalPrice': total_price,
                        'components': [
                            {
                                'name': f"{comp.manufacturer.name} {comp.model}",
                                'price': comp.price,
                                'category': next((name for id, name in category_ids if id == comp.category_id), ''),
                                'country': comp.country_of_origin,  # Используем поле country_of_origin
                                'link': comp.link_to_store
                            }
                            for comp in current_build
                        ]
                    })
                    return

                components = category_components[cats[category_index] - 1]

                # Пытаемся выбрать самый дорогой вариант, который вписывается в бюджет
                for comp in components:
                    if comp.price <= remaining_budget:
                        # Выбираем этот компонент и переходим к следующей категории
                        backtrack(
                            current_build + [comp],
                            remaining_budget - comp.price,
                            category_index + 1,
                            current_components
                        )
                else:
                    # Не нашли подходящий компонент - возвращаемся к предыдущей категории
                    return

            # Начинаем поиск с пустой сборки и полного бюджета
            backtrack([], budget, 0, category_components)
            return builds

        category_ids = [
            (1, "Процессоры"),
            (2, "Видеокарты"),
            (3, "Материнские платы"),
            (4, "Оперативная память"),
            (5, "Накопители SSD"),
            (7, "Блоки питания"),
            (8, "Корпуса"),
            (9, "Системы охлаждения"),
        ]

        builds = generate_builds()
        print(builds)
        if not builds:
            return Response({'error': 'Не удалось собрать конфигурацию в заданный бюджет'}, status=400)
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
